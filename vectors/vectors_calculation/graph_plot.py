processed_outputs = [] # Renamed from processed_results to avoid confusion
print("--- Processing AI Results for Plotting ---")
for ai_result_string in results: # Assuming 'results' is the list of AI output strings
    print(f"\nInput string from AI: {ai_result_string}")
    data_for_plot = process_vector_query(ai_result_string)
    processed_outputs.append(data_for_plot)
    
    # You can print the dictionary to see what process_vector_query returned:
    # import json
    # print(f"Processed data: {json.dumps(data_for_plot, indent=2, default=str)}") # Using json for pretty print

    if data_for_plot.get("error_message"):
        print(f"  Error encountered: {data_for_plot['error_message']}")
        # Optionally, still try to plot if there are input vectors, or skip plotting
        # For now, the plotting function will display the error as title
        plot_vector_data(data_for_plot)
    else:
        print(f"  Operation: {data_for_plot['operation_name']}")
        print(f"  Display Message: {data_for_plot['display_message']}")
        plot_vector_data(data_for_plot)
    print("-" * 30)
