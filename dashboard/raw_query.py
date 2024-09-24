from django.db import connection


def get_dashboard_data():
    with connection.cursor() as cursor:
        sql = """
        select
        (select count(id) from products_category where is_active = true) as category_count,
        (select count(id) from products_product where is_active = true) as product_count,
        (select count(id) from products_supplier where is_active = true) as supplier_count,
        (select sum(i.qty) from inventory_transaction it inner join public.inventory_transactionitem i
                on it.id = i.transaction_id
                    where transaction_type_id = 2) as sales_qty_count,
        (select sum(i.qty) from inventory_transaction it inner join public.inventory_transactionitem i
                    on it.id = i.transaction_id
                        where transaction_type_id = 1) as purchase_qty_count,
        (select sum(total_amount) from inventory_transaction where transaction_type_id = 2 ) as total_sales_amount,
        (select sum(total_amount) from inventory_transaction where transaction_type_id = 1 ) as total_purchase_amount;
        """
        cursor.execute(sql)
        rows = cursor.fetchone()

        # Get column names from the cursor
        columns = [col[0] for col in cursor.description]

        # Convert the rows into a list of dictionaries
        result = dict(zip(columns, rows))
        return result