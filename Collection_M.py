
from bs4 import BeautifulSoup
import os
import pandas as pd

data = {'Society_Name': [], 'Locality': [], 'Price': [], 'Average Price': [], 'BHK Type': [], 'Area': [], 'Possession Status': []}

base_dir = r"C:\Users\salam_jmvmbso\OneDrive\Desktop\Data Scraping\MagicBrick\Magicbricks_data"

if not os.path.exists(base_dir):
    print(f"Directory not found: {base_dir}")
else:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    html_doc = f.read()
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    
                    title = soup.find("div", class_="mb-srp__card__developer")
                    society_name = title.get_text(strip=True) if title else "N/A"
                    data['Society_Name'].append(society_name)
                  
                    locality_tag = soup.find("h2", class_="mb-srp__card--title")
                    locality = locality_tag.get_text(strip=True).split(" in ")[-1] if locality_tag else "N/A"
                    data['Locality'].append(locality)

                    price_tag = soup.find("div", class_="mb-srp__card__price--amount")
                    price = price_tag.get_text(strip=True) if price_tag else "N/A"
                    data['Price'].append(price)

                    avg_price_tag = soup.find("div", class_="mb-srp__card__price--size")
                    avg_price = avg_price_tag.get_text(strip=True) if avg_price_tag else "N/A"
                    data['Average Price'].append(avg_price)

                    bhk_tag = soup.find("h2", class_="mb-srp__card--title")
                    bhk_type = bhk_tag.get_text(strip=True).split("Flat")[0].strip() if bhk_tag else "N/A"
                    data['BHK Type'].append(bhk_type)

                    area_tag = soup.find("div", class_="mb-srp__card__summary__list").find("div", class_="mb-srp__card__summary--value")
                    area = area_tag.get_text(strip=True) if area_tag else "N/A"
                    data['Area'].append(area)
                    
                    summary_list = soup.find("div", class_="mb-srp__card__summary__list")
                    if summary_list:
                        status_tag = summary_list.find("div", {'data-summary': 'status'})
                        possession_status = status_tag.find("div", class_="mb-srp__card__summary--value").get_text(strip=True) if status_tag else "N/A"
                        data['Possession Status'].append(possession_status)
                    else:
                        data['Possession Status'].append("N/A")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    df = pd.DataFrame(data)
    csv_path = "magicbricks_data.csv"

    try:
        df.to_csv(csv_path, index=False)
        print(f"CSV file created successfully: {csv_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

    print(df)
