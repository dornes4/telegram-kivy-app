from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
import json
import threading
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

TON_TO_USD_RATE = 2.75
JOINED_LINKS_COL_IDX = 2
SPENT_LINKS_COL_IDX = 3
START_COL_IDX = 11
MAX_DAYS = 31
CREDENTIALS_FILE = "credentials.json"

class RootWidget(BoxLayout):
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def update_analytics(self):
        try:
            cookies1 = json.loads(self.ids.cookies1.text)
            cookies2 = json.loads(self.ids.cookies2.text)
            spreadsheet = self.ids.spreadsheet.text
            worksheet = self.ids.worksheet.text
        except Exception as e:
            self.show_popup("Ошибка", f"Неверный JSON: {e}")
            return

        def run():
            try:
                creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=[
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive',
                ])
                gc = gspread.authorize(creds)
                ws = gc.open(spreadsheet).worksheet(worksheet)

                joined_links = ws.col_values(JOINED_LINKS_COL_IDX)[2:]
                spent_links = ws.col_values(SPENT_LINKS_COL_IDX)[2:]

                max_cols = ws.col_count
                needed_cols = START_COL_IDX - 1 + 5 * MAX_DAYS
                if max_cols < needed_cols:
                    ws.add_cols(needed_cols - max_cols)

                START_DATE = datetime.strptime("20 Jun 2025", "%d %b %Y")
                END_DATE = datetime.strptime("20 Jul 2025", "%d %b %Y")
                all_dates = [(START_DATE + timedelta(days=i)).strftime("%d %b %Y") for i in range((END_DATE - START_DATE).days + 1)]

                def colnum_string(n):
                    string = ""
                    while n > 0:
                        n, remainder = divmod(n - 1, 26)
                        string = chr(65 + remainder) + string
                    return string

                def download_csv_auth(url, cookies):
                    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, cookies=cookies)
                    resp.raise_for_status()
                    return resp.text

                def parse_csv_to_dict(csv_text, value_col_name):
                    lines = csv_text.strip().split('\n')
                    header_line = lines[0]
                    delimiter = '\t' if '\t' in header_line else ',' if ',' in header_line else None
                    if not delimiter:
                        return {}
                    header = header_line.split(delimiter)
                    date_idx = next((i for i, h in enumerate(header) if h.strip().lower() in ['date', 'day']), None)
                    val_idx = next((i for i, h in enumerate(header) if h.strip().lower() == value_col_name.lower()), None)
                    if date_idx is None or val_idx is None:
                        return {}
                    data = {}
                    for line in lines[1:]:
                        parts = line.split(delimiter)
                        if len(parts) <= max(date_idx, val_idx):
                            continue
                        date = parts[date_idx].strip()
                        if date.lower().startswith('total'):
                            continue
                        val_str = parts[val_idx].replace(',', '.').strip()
                        try:
                            val = float(val_str)
                        except:
                            val = 0
                        data[date] = val
                    return data

                start_letter = colnum_string(START_COL_IDX)
                end_letter = colnum_string(START_COL_IDX + len(all_dates) * 5 - 1)

                ws.update(f"{start_letter}1:{end_letter}1", [[d for date in all_dates for d in [date, '', '', '', '']]])
                ws.update(f"{start_letter}2:{end_letter}2", [["Spent (USD)", "Joined", "Цена пдп", "Приватных подписчиков", "Цена приват"] * len(all_dates)])
                ws.update("G2", [["Затраты"]])
                ws.update("H2", [["ПДП"]])
                ws.update("I2", [["Цена пдп"]])

                for row_idx, (joined_cell, spent_cell) in enumerate(zip(joined_links, spent_links), start=3):
                    joined_urls = [url.strip() for url in joined_cell.split(',') if url.strip()]
                    spent_urls = [url.strip() for url in spent_cell.split(',') if url.strip()]

                    def gather_data(urls, value_names):
                        aggregated = {}
                        for url in urls:
                            for cookies in [cookies1, cookies2]:
                                for val_name in value_names:
                                    try:
                                        csv_text = download_csv_auth(url, cookies)
                                        data = parse_csv_to_dict(csv_text, val_name)
                                        if data:
                                            for k, v in data.items():
                                                aggregated[k] = aggregated.get(k, 0) + v
                                            break
                                    except:
                                        continue
                        return aggregated

                    joined_data = gather_data(joined_urls, ['joined', 'started bot'])
                    spent_data = gather_data(spent_urls, ['spent budget, ton', 'amount, ton'])

                    row_values = []
                    total_spent_usd = 0
                    total_joined = 0

                    for date in all_dates:
                        spent_val = spent_data.get(date, 0)
                        joined_val = joined_data.get(date, 0)
                        spent_usd = spent_val * TON_TO_USD_RATE
                        total_spent_usd += spent_usd
                        total_joined += joined_val
                        row_values.extend([
                            f"{spent_usd:.2f}$",
                            int(joined_val) if joined_val else '',
                            '', '', ''
                        ])

                    ws.update(f"{start_letter}{row_idx}:{end_letter}{row_idx}", [row_values])
                    ws.update(f"G{row_idx}", [[f"{total_spent_usd:.2f}".replace('.', ',')]])
                    ws.update(f"H{row_idx}", [[int(total_joined) if total_joined else '']])
                    if total_joined > 0:
                        price_per_join = total_spent_usd / total_joined
                        ws.update(f"I{row_idx}", [[f"{price_per_join:.2f}".replace('.', ',')]])
                    else:
                        ws.update(f"I{row_idx}", [['']])
                self.show_popup("Готово", "Аналитика обновлена!")
            except Exception as e:
                self.show_popup("Ошибка", str(e))

        threading.Thread(target=run, daemon=True).start()

class TelegramApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    TelegramApp().run()
