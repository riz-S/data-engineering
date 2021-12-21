import great_expectations as ge

# Menjalankan checkpoint setiap setelah ETL
context = ge.get_context()
context.run_checkpoint(checkpoint_name="tweet-checking")