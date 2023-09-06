import pandas as pd
import fundamentalanalysis as fa
from matplotlib import pyplot as plt
import numpy as np
import csv
import os
import streamlit as st

directory = os.getcwd()
st.text(f'Running in {directory}')
st.title("Rentabilitets analyse")
st.markdown("Dette program er udviklet til at udregne rentabilitet for en virksomhed, samtidig med at analysere disse nøgletal med en standard for branchen. Følg instruktionerne nedenfor for at komme i gang.")

ticker = st.text_input("Input virksomheds ticker")
peers_input = st.text_input("Input relevante peers. Seperate med komma", 'JBHT, DFDS.co, XPO, ARCB, WERN')
st.markdown("Hvilke plots er du interreseret i? Inkluder dem herunder.")
aoh_choice = st.checkbox("Aktivernes omsætningshastighed plot", value=False)
og_choice = st.checkbox("Overskudsgrad plot", value=False)
ag_choice = st.checkbox("Afkastningsgrad plot", value=False)
ekf_choice = st.checkbox("Egenkapitalsforrentning plot", value=False)
sg_choice = st.checkbox("Soliditetsgrad plot", value=False)

state1 = st.button("Generer plots")

if state1:
   loop_count = 0

   og_peers = []
   aoh_peers = []
   ag_peers = []
   ekf_peers = []
   sg_peers = []

   api_key1 = "01fae01643f648ade90c7855543840a2" # 250 left
   api_key2 = "5903081af36d587607a68b06c417afd6" # 250 left
   api_key3 = "41d221e22556d9d37afed403b6ec195f" # Empty for this month



   # Make streamlit input that splits user input into a list of tickers
   peers = list(peers_input.split(', '))

   main_company_og = []
   main_company_aoh = []
   main_company_ag = []
   main_company_ekf = []
   main_company_sg = []


   # Raw numbers
   print(peers)
   for company in peers:
      try:
         if company == peers[0]:
            income_statement_annually = fa.income_statement(ticker, api_key1, period="annual")
            balance_sheet_annually = fa.balance_sheet_statement(ticker, api_key1, period="annual")

            ebit_timeline = []
            year = 2022

            income_statement_annually = fa.income_statement(ticker, api_key1, period="annual")
            balance_sheet_annually = fa.balance_sheet_statement(ticker, api_key1, period="annual")

            ebit_timeline = []
            year = 2022
            for x in range(4):
                  temp_year = str(year - x)
                  ebit_timeline.append(income_statement_annually[temp_year]['ebitda'] - income_statement_annually[temp_year]['depreciationAndAmortization'])
                  
            asset_timeline = []
            for x in range(4):
                  temp_year = str(year - x)
                  asset_timeline.append(balance_sheet_annually[temp_year]['totalAssets'])

            revenue_timeline = []
            for x in range(4):
                  temp_year = str(year - x)
                  revenue_timeline.append(income_statement_annually[temp_year]['revenue'])
                  
            result_timeline = []
            for x in range(4):
                  temp_year = str(year - x)
                  result_timeline.append(income_statement_annually[temp_year]['incomeBeforeTax'])

            equity_timeline = []
            for x in range(4):
                  temp_year = str(year - x)
                  equity_timeline.append(balance_sheet_annually[temp_year]['totalEquity'])
                  
            netdebt_timeline = []
            for x in range(4):
                  temp_year = str(year - x)
                  netdebt_timeline.append(balance_sheet_annually[temp_year]['netDebt'])

            # OG
            main_company_og = []
            for x in range(4):
                  main_company_og.append(ebit_timeline[x] / revenue_timeline[x])

            # AOH
            main_company_aoh = []
            for x in range(4):
                  main_company_aoh.append(revenue_timeline[x] / asset_timeline[x])

            # AG
            main_company_ag = []
            for x in range(4):
                  main_company_ag.append(ebit_timeline[x] / asset_timeline[x])

            # EKF
            main_company_ekf = []
            for x in range(4):
                  main_company_ekf.append(result_timeline[x] / asset_timeline[x])

            # SG
            main_company_sg = []
            for x in range(4):
                  main_company_sg.append(equity_timeline[x] / asset_timeline[x])

         income_statement_annually = fa.income_statement(company, api_key1, period="annual")
         balance_sheet_annually = fa.balance_sheet_statement(company, api_key1, period="annual")

         ebit_timeline = []
         year = 2022
         for x in range(4):
            temp_year = str(year - x)
            ebit_timeline.append(income_statement_annually[temp_year]['ebitda'] - income_statement_annually[temp_year]['depreciationAndAmortization'])
         
         asset_timeline = []
         for x in range(4):
            temp_year = str(year - x)
            asset_timeline.append(balance_sheet_annually[temp_year]['totalAssets'])

         revenue_timeline = []
         for x in range(4):
            temp_year = str(year - x)
            revenue_timeline.append(income_statement_annually[temp_year]['revenue'])
         
         result_timeline = []
         for x in range(4):
            temp_year = str(year - x)
            result_timeline.append(income_statement_annually[temp_year]['incomeBeforeTax'])

         equity_timeline = []
         for x in range(4):
            temp_year = str(year - x)
            equity_timeline.append(balance_sheet_annually[temp_year]['totalEquity'])
         
         netdebt_timeline = []
         for x in range(4):
            temp_year = str(year - x)
            netdebt_timeline.append(balance_sheet_annually[temp_year]['netDebt'])

         # OG
         temp_lst = []
         for x in range(4):
            temp_lst.append(ebit_timeline[x] / revenue_timeline[x])
         
         og_peers.append(temp_lst)
         
         # AOH
         temp_lst = []
         for x in range(4):
            temp_lst.append(revenue_timeline[x] / asset_timeline[x])
         
         aoh_peers.append(temp_lst)

         # AG
         temp_lst = []
         for x in range(4):
            temp_lst.append(ebit_timeline[x] / asset_timeline[x])
         
         ag_peers.append(temp_lst)

         # EKF
         temp_lst = []
         for x in range(4):
            temp_lst.append(result_timeline[x] / asset_timeline[x])
         
         ekf_peers.append(temp_lst)

         # SG
         temp_lst = []
         for x in range(4):
            temp_lst.append(equity_timeline[x] / asset_timeline[x])
         
         sg_peers.append(temp_lst)

         loop_count += 1
         print(f'Looped through {loop_count} companies')
      except Exception as e:
         print(e)

   sum = 0

   og_peers_average = []
   aoh_peers_average = []
   ag_peers_average = []
   ekf_peers_average = []
   sg_peers_average = []

   #Averages
   print(og_peers)
   for y in range(len(og_peers[0])):
      tempsum = 0
      for x in range(len(og_peers)):
         print(x)
         print(y)
         tempsum += og_peers[x][y]

      og_peers_average.append(tempsum / len(og_peers))

      tempsum = 0
      for x in range(len(aoh_peers)):
         tempsum += aoh_peers[x][y]

      aoh_peers_average.append(tempsum / len(og_peers))

      tempsum = 0
      for x in range(len(ag_peers)):
         tempsum += ag_peers[x][y]

      ag_peers_average.append(tempsum / len(og_peers))

      tempsum = 0
      for x in range(len(ekf_peers)):
         tempsum += ekf_peers[x][y]

      ekf_peers_average.append(tempsum / len(og_peers))

      tempsum = 0

      for x in range(len(sg_peers)):
         tempsum += sg_peers[x][y]

      sg_peers_average.append(tempsum / len(og_peers))

   # PLOT AOH
   if aoh_choice:
      st.text("Plot for AOH")
      fig, ax1 = plt.subplots()

      print(main_company_aoh)
      plt.plot([2022, 2021, 2020, 2019], main_company_aoh, 'b-..', color='blue', label=str(ticker))

      control = 0
      for company_lst in aoh_peers:
         plt.plot([2022, 2021, 2020, 2019], company_lst, 'b-..', color='green', alpha=0.1) # label=str(peers[control])
         control += 1

      print(aoh_peers)
      plt.plot([2022, 2021, 2020, 2019], aoh_peers_average, color='green', label='Gnms. AOH for peers') # aoh_peers_average

      # plt.plot([2022, 2021, 2020, 2019], [0.0784,0.0520,0.048,0.05], color='red', label='Afkastkrav CoE')
      # plt.plot([2022, 2021, 2020, 2019], [0.35,0.35,0.35,0.35,], color='red', label='Rentabilitetshensyn')

      ax1.set_xlabel('Årstal')
      plt.xticks(np.arange(2019, 2022+1, 1))

      ax1.set_ylabel('AOH som g-faktor')

      plt.title(f'Udvikling i AOH for {ticker} og peers')
      plt.legend()
      fig.tight_layout()

      plt.show()
      st.pyplot(fig)
   
   # PLOT OG
   if og_choice:
      st.text("Plot for OG")
      fig, ax1 = plt.subplots()

      print(main_company_og)
      plt.plot([2022, 2021, 2020, 2019], main_company_og, 'b-..', color='blue', label=str(ticker))

      control = 0
      for company_lst in og_peers:
         plt.plot([2022, 2021, 2020, 2019], company_lst, 'b-..', color='green', alpha=0.1) # label=str(peers[control])
         control += 1

      print(og_peers)
      plt.plot([2022, 2021, 2020, 2019], og_peers_average, color='green', label='Gnms. OG for peers') # aoh_peers_average

      # plt.plot([2022, 2021, 2020, 2019], [0.0784,0.0520,0.048,0.05], color='red', label='Afkastkrav CoE')
      # plt.plot([2022, 2021, 2020, 2019], [0.35,0.35,0.35,0.35,], color='red', label='Rentabilitetshensyn')

      ax1.set_xlabel('Årstal')
      plt.xticks(np.arange(2019, 2022+1, 1))

      ax1.set_ylabel('OG som decimaltal')

      plt.title(f'Udvikling i OG for {ticker} og peers')
      plt.legend()
      fig.tight_layout()

      plt.show()
      st.pyplot(fig)

   # PLOT AG
   if ag_choice:
      st.text("Plot for AG")
      fig, ax1 = plt.subplots()

      print(main_company_ag)
      plt.plot([2022, 2021, 2020, 2019], main_company_ag, 'b-..', color='blue', label=str(ticker))

      control = 0
      for company_lst in ag_peers:
         plt.plot([2022, 2021, 2020, 2019], company_lst, 'b-..', color='green', alpha=0.1) # label=str(peers[control])
         control += 1

      print(ag_peers)
      plt.plot([2022, 2021, 2020, 2019], ag_peers_average, color='green', label='Gnms. AG for peers') # aoh_peers_average

      plt.plot([2022, 2021, 2020, 2019], [0.0784,0.0520,0.048,0.05], color='red', label='Afkastkrav CoE')
      # plt.plot([2022, 2021, 2020, 2019], [0.35,0.35,0.35,0.35,], color='red', label='Rentabilitetshensyn')

      ax1.set_xlabel('Årstal')
      plt.xticks(np.arange(2019, 2022+1, 1))

      ax1.set_ylabel('AG som decimaltal')

      plt.title(f'Udvikling i AG for {ticker} og peers')
      plt.legend()
      fig.tight_layout()

      plt.show()
      st.pyplot(fig)
   
   # PLOT EKF
   if ekf_choice:
      st.text("Plot for EKF")
      fig, ax1 = plt.subplots()

      print(main_company_ekf)
      plt.plot([2022, 2021, 2020, 2019], main_company_ekf, 'b-..', color='blue', label=str(ticker))

      control = 0
      for company_lst in ekf_peers:
         plt.plot([2022, 2021, 2020, 2019], company_lst, 'b-..', color='green', alpha=0.1) # label=str(peers[control])
         control += 1

      print(ekf_peers)
      plt.plot([2022, 2021, 2020, 2019], ekf_peers_average, color='green', label='Gnms. EKF for peers') # aoh_peers_average

      plt.plot([2022, 2021, 2020, 2019], [0.0784,0.0520,0.048,0.05], color='red', label='Afkastkrav CoE')
      # plt.plot([2022, 2021, 2020, 2019], [0.35,0.35,0.35,0.35,], color='red', label='Rentabilitetshensyn')

      ax1.set_xlabel('Årstal')
      plt.xticks(np.arange(2019, 2022+1, 1))

      ax1.set_ylabel('EKF som decimaltal')

      plt.title(f'Udvikling i EKF for {ticker} og peers')
      plt.legend()
      fig.tight_layout()

      plt.show()
      st.pyplot(fig)