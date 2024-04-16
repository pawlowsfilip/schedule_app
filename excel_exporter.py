import pandas as pd
import xlsxwriter


class ExcelExporter:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def schedule_to_dataframe(self):
        data = []
        for day, time_frames in self.scheduler.items():
            for time_frame, workers in time_frames.items():
                worker_names = ', '.join([worker.name for worker in workers]) if workers else "No worker"
                data.append({'Date': day, 'Time Frame': time_frame, 'Workers': worker_names})
        return pd.DataFrame(data)

    def pivot_schedule(self):
        df = self.schedule_to_dataframe()
        # Pivot the table
        pivot_df = df.pivot(index='Time Frame', columns='Date', values='Workers')
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None  # Remove the hierarchy on the columns
        return pivot_df

    def export_to_excel(self, filename='schedule.xlsx'):
        df = self.pivot_schedule()  # Use the pivoted DataFrame
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Schedule', header=False)

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
