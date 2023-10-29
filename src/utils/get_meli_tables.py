from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def get_meli_tables(driver, wait):
    classes = {
        "andes": 'andes-table',
        "striped": 'ui-vpp-striped-specs__table'
    }

    tables = []

    try:
        andes_tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, classes['andes'])))
        tables.extend(andes_tables)
    except NoSuchElementException:
        pass

    try:
        striped_tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, classes['striped'])))
        tables.extend(striped_tables)
    except NoSuchElementException:
        pass

    return tables
