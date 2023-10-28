from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def browser(ecommerce,url):
    if ecommerce == "meli":
        return navigate_meli(url)
    return 



def navigate_meli(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Initiate the browser
    driver = webdriver.Chrome(options=chrome_options)
    
    # Navigate to the URL
    driver.get(url)
    
    # Implicitly wait (wait for elements to load)
    driver.implicitly_wait(5)

    fetched_tables = []

    try:
        print("Fetching tables directly from the HTML...")
        tables = driver.find_elements_by_xpath('//table[@class="andes-table"]')
        title = driver.find_elements_by_xpath('//h1[@class="ui-pdp-title"]')
        if tables:
            print(f"Found {len(tables)} tables.")
            for table in tables:
                fetched_tables.append(table.get_attribute('outerHTML'))
        else:
            print("No tables found.")
        
        transformed_tables = meli_tables_to_json(fetched_tables)
        
        title_text = title[0].text if title else None
        data = {
            'product': title_text,
            'detail': transformed_tables
            }

        return data

    except Exception as e:
        print(f"Error encountered: {e}")

    finally:
        # Always close the driver
        driver.quit()

def meli_tables_to_json(tables_html):
    """
    Convert list of tables' outerHTML to a JSON structure.
    """
    table_data = []

    for table_html in tables_html:
        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
        table_dict = {"headers": [], "rows": []}

        # Extract headers
        headers = table.find_all("th")
        for header in headers:
            table_dict["headers"].append(header.text)

        # Extract rows
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            row_data = [cell.text for cell in cells]
            if row_data:  # Check if row_data is not empty
                table_dict["rows"].append(row_data)

        table_data.append(table_dict)
    table_data = transform_structure(table_data)

    return table_data

def transform_structure(tables):
    """
    Transforms the table data into the desired JSON structure.
    """
    result = []

    for index, table in enumerate(tables):
        table_dict = {}
        for i, header in enumerate(table["headers"]):
            value = table["rows"][i][0] if i < len(table["rows"]) else None
            table_dict[header] = value
        result.append({f"table_{index + 1}": table_dict})

    return result
