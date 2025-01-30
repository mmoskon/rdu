import streamlit as st
import pandas as pd
import io

def get_excel_file(df):

    # Convert DataFrame to Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()

    # Get the Excel file as bytes
    excel_data = output.getvalue()
    return excel_data


fdata = st.file_uploader("Naloži Excel", type={"xlsx"})


if fdata:

    df = pd.read_excel(fdata, skiprows=3)
    idx_max = int(df.columns[-1].split(" ")[1])


    for i in range(idx_max):
        cost = df[f"% {i+1:02d}"] * df['Znesek RDU'] / 100
        PPS = df[f"PSP {i+1:02d}"]
        PI = df["Priimek in ime"]


        df_costs2 = pd.DataFrame(columns=['PI', 'PPS', 'znesek'])
        df_costs2['PI'] = PI
        df_costs2['PPS'] = PPS
        df_costs2['znesek'] = cost

        df_costs2.dropna(axis=0, how="any", inplace=True)

        if i == 0:
            df_costs = df_costs2
        else:
            df_costs = pd.concat((df_costs, df_costs2), ignore_index=True)

    df_summed = df_costs.groupby("PPS", as_index=False)["znesek"].sum()
    #df_summed.to_excel(f"{f_name}_costs_PPS.xlsx", index=False)

    # Download button
    st.download_button(
        label="Download Excel File",
        data=get_excel_file(df_summed),
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )