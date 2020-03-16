from io_interface import save_reports_in_csv, get_report_path, go_through_files, get_args

args = get_args()
report_path = get_report_path(args.output)
report = go_through_files(args.input, args.output)
save_reports_in_csv(report_path, report)

print('Report created!')
