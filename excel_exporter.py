import pandas as pd
import xlsxwriter
from datetime import datetime

class ExcelExporter:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    @staticmethod
    def parse_time_frame_key(time_frame):
        start_str, _ = time_frame.split('-')
        return datetime.strptime(start_str.strip(), '%H:%M')

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str.strip(), '%d.%m')

    def schedule_to_dataframe(self):
        data = []
        sorted_data = []

        for day, time_frames in self.scheduler.items():
            for time_frame in time_frames.keys():
                sorted_data.append((day, time_frame))

        sorted_data.sort(key=lambda x: (self.parse_date(x[0]), self.parse_time_frame_key(x[1])))

        for day, time_frame in sorted_data:
            workers = self.scheduler[day][time_frame]
            worker_names = ', '.join([worker.name for worker in workers if hasattr(worker, 'name')]) or "No worker"
            data.append({'Date': day, 'Time Frame': time_frame, 'Workers': worker_names})

        return pd.DataFrame(data)

    def pivot_schedule(self):
        df = self.schedule_to_dataframe()
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')
        df.sort_values(by=['Date', 'Time Frame'], inplace=True)
        df['Date'] = df['Date'].dt.strftime('%d.%m')

        time_frames_ordered = sorted(df['Time Frame'].unique(), key=lambda x: self.parse_time_frame_key(x))

        pivot_df = df.pivot(index='Time Frame', columns='Date', values='Workers')

        pivot_df = pivot_df.reindex(index=time_frames_ordered)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None

        print('Pivoted DataFrame:\n', pivot_df)
        return pivot_df

    def export_to_excel(self, filename='schedule.xlsx'):
        df = self.pivot_schedule()
        df.fillna('', inplace=True)  # Replace NaN with empty string
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Schedule')

            workbook = writer.book
            worksheet = writer.sheets['Schedule']

            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'fg_color': '#D7E4BC',
                'align': 'center',
                'border': 2
            })

            cell_format = workbook.add_format({
                'border': 1
            })

            bold_border_format = workbook.add_format({
                'border': 2
            })

            # Setting header properties
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # setting cell properties
            for row_num in range(1, len(df) + 1):
                for col_num in range(len(df.columns)):
                    cell_value = df.iloc[row_num - 1, col_num]
                    worksheet.write(row_num, col_num, cell_value, cell_format)

            # Setting bold border for whole table
            last_row, last_col = len(df), len(df.columns) - 1
            worksheet.conditional_format(0, 0, last_row, last_col, {
                'type': 'no_errors',
                'format': bold_border_format
            })

            worksheet.autofit()
            print('schedule exported to {}'.format(filename))