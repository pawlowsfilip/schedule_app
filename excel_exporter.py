import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExcelExporter:
    def __init__(self, scheduler):
        try:
            logger.debug("Initializing the ExcelExporter")
            self.scheduler = scheduler
            logger.info("ExcelExporter initialized with a scheduler.")
        except Exception as e:
            logger.error(f"Error initializing ExcelExporter: {e}")

    @staticmethod
    def parse_time_frame_key(time_frame):
        try:
            start_str, _ = time_frame.split('-')
            time_obj = datetime.strptime(start_str.strip(), '%H:%M')
            logger.debug(f"Parsed time frame key: {time_frame} into {time_obj}.")
            return time_obj
        except ValueError as e:
            logger.error(f"Error parsing time frame: {time_frame}. Exception: {e}")

    @staticmethod
    def parse_date(date_str):
        try:
            date_obj = datetime.strptime(date_str.strip(), '%d.%m')
            logger.debug(f"Parsed date: {date_str} into {date_obj}.")
            return date_obj
        except ValueError as e:
            logger.error(f"Error parsing date: {date_str}. Exception: {e}")

    def schedule_to_dataframe(self):
        data = []
        sorted_data = []

        logger.debug("Converting schedule to DataFrame.")
        try:
            for day, time_frames in self.scheduler.items():
                for time_frame in time_frames.keys():
                    sorted_data.append((day, time_frame))

            sorted_data.sort(key=lambda x: (self.parse_date(x[0]), self.parse_time_frame_key(x[1])))
            logger.debug(f"Sorted schedule data: {sorted_data}.")

            for day, time_frame in sorted_data:
                workers = self.scheduler[day][time_frame]
                worker_names = ', '.join([worker if isinstance(worker, str) else worker.name for worker in workers])
                data.append({'Date': day, 'Time Frame': time_frame, 'Workers': worker_names})

            logger.info(f"Converted schedule to DataFrame successfully: {data}.")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error converting schedule to DataFrame: {e}")
            return pd.DataFrame()

    def pivot_schedule(self):
        logger.debug("Pivoting schedule.")
        df = self.schedule_to_dataframe()
        if df.empty:
            logger.error("Schedule is empty. Cannot pivot.")
            return pd.DataFrame()
        try:
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')
            df.sort_values(by=['Date', 'Time Frame'], inplace=True)
            df['Date'] = df['Date'].dt.strftime('%d.%m')

            time_frames_ordered = sorted(df['Time Frame'].unique(), key=lambda x: self.parse_time_frame_key(x))

            pivot_df = df.pivot(index='Time Frame', columns='Date', values='Workers')

            pivot_df = pivot_df.reindex(index=time_frames_ordered)
            pivot_df.reset_index(inplace=True)
            pivot_df.columns.name = None

            logger.info(f"Pivoted the schedule successfully:\n{pivot_df}.")
            return pivot_df
        except Exception as e:
            logger.error(f"Error pivoting the schedule: {e}")

    def export_to_excel(self, filename='schedule.xlsx'):
        logger.debug(f"Exporting schedule to Excel: {filename}.")
        df = self.pivot_schedule()
        df.fillna('', inplace=True)  # Replace NaN with empty string

        try:
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

                last_row, last_col = len(df), len(df.columns) - 1

                worksheet.conditional_format(1, 0, last_row, last_col, {
                    'type': 'cell',
                    'criteria': 'equal to',
                    'value': '"NO WORKER AVAILABLE"',
                    'format': workbook.add_format({'font_color': 'red'})
                })

                worksheet.conditional_format(1, 0, last_row, last_col, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'NO WORKER',
                    'format': workbook.add_format({'font_color': '#b08c09'})
                })

                worksheet.conditional_format(1, 0, last_row, last_col, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': '-',
                    'format': workbook.add_format({'font_color': 'black'})
                })

                worksheet.conditional_format(1, 0, last_row, last_col, {
                    'type': 'text',
                    'criteria': 'not containing',
                    'value': 'NO WORKER',
                    'format': workbook.add_format({'font_color': 'green'})
                })

                worksheet.conditional_format(0, 0, last_row, last_col, {
                    'type': 'no_errors',
                    'format': bold_border_format
                })

                worksheet.autofit()
                logger.info(f"Schedule exported to {filename} successfully.")
        except Exception as e:
            logger.error(f"Error occurred while exporting to Excel: {e}")
