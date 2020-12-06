# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http://www.cs.brown.edu/~pavlo/
#
# Original Java Version:
# Copyright (C) 2008
# Evan Jones
# Massachusetts Institute of Technology
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------

MONEY_DECIMALS = 2

#  Item constants
NUM_ITEMS = 100000
MIN_IM = 1
MAX_IM = 10000
MIN_PRICE = 1.00
MAX_PRICE = 100.00
MIN_I_NAME = 14
MAX_I_NAME = 24
MIN_I_DATA = 26
MAX_I_DATA = 50

#  Warehouse constants
MIN_TAX = 0
MAX_TAX = 0.2000
TAX_DECIMALS = 4
INITIAL_W_YTD = 300000.00
MIN_NAME = 6
MAX_NAME = 10
MIN_STREET = 10
MAX_STREET = 20
MIN_CITY = 10
MAX_CITY = 20
STATE = 2
ZIP_LENGTH = 9
ZIP_SUFFIX = "11111"

#  Stock constants
MIN_QUANTITY = 10
MAX_QUANTITY = 100
DIST = 24
STOCK_PER_WAREHOUSE = 100000

#  District constants
DISTRICTS_PER_WAREHOUSE = 10
INITIAL_D_YTD = 30000.00  #  different from Warehouse
INITIAL_NEXT_O_ID = 3001

#  Customer constants
CUSTOMERS_PER_DISTRICT = 3000
INITIAL_CREDIT_LIM = 50000.00
MIN_DISCOUNT = 0.0000
MAX_DISCOUNT = 0.5000
DISCOUNT_DECIMALS = 4
INITIAL_BALANCE = -10.00
INITIAL_YTD_PAYMENT = 10.00
INITIAL_PAYMENT_CNT = 1
INITIAL_DELIVERY_CNT = 0
MIN_FIRST = 6
MAX_FIRST = 10
MIDDLE = "OE"
PHONE = 16
MIN_C_DATA = 300
MAX_C_DATA = 500
GOOD_CREDIT = "GC"
BAD_CREDIT = "BC"

#  Order constants
MIN_CARRIER_ID = 1
MAX_CARRIER_ID = 10
#  HACK: This is not strictly correct, but it works
NULL_CARRIER_ID = 0
#  o_id < than this value, carrier != null, >= -> carrier == null
NULL_CARRIER_LOWER_BOUND = 2101
MIN_OL_CNT = 5
MAX_OL_CNT = 15
INITIAL_ALL_LOCAL = 1
INITIAL_ORDERS_PER_DISTRICT = 3000

#  Used to generate new order transactions
MAX_OL_QUANTITY = 10

#  Order line constants
INITIAL_QUANTITY = 5
MIN_AMOUNT = 0.01

#  History constants
MIN_DATA = 12
MAX_DATA = 24
INITIAL_AMOUNT = 10.00

#  New order constants
INITIAL_NEW_ORDERS_PER_DISTRICT = 900

#  TPC-C 2.4.3.4 (page 31) says this must be displayed when new order rolls back.
INVALID_ITEM_MESSAGE = "Item number is not valid"

#  Used to generate stock level transactions
MIN_STOCK_LEVEL_THRESHOLD = 10
MAX_STOCK_LEVEL_THRESHOLD = 20

#  Used to generate payment transactions
MIN_PAYMENT = 1.0
MAX_PAYMENT = 5000.0

#  Indicates "brand" items and stock in i_data and s_data.
ORIGINAL_STRING = "ORIGINAL"

# Query
QUERIES = {
    "q1": '''
        select
            l_returnflag,
            l_linestatus,
            sum(l_quantity) as sum_qty,
            sum(l_extendedprice) as sum_base_price,
            sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
            sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
            avg(l_quantity) as avg_qty,
            avg(l_extendedprice) as avg_price,
            avg(l_discount) as avg_disc,
            count(l_quantity) as count_order
        from
            lineitem
        where
            l_shipdate <= date '1998-12-01' - interval '117' day
        group by
            l_returnflag,
            l_linestatus
        order by
            l_returnflag,
            l_linestatus
        limit 1;''',
    "q2": '''
        select
            s_acctbal,
            s_name,
            n_name,
            p_partkey,
            p_mfgr,
            s_address,
            s_phone,
            s_comment
        from
            part,
            supplier,
            partsupp,
            nation,
            region
        where
            p_partkey = ps_partkey
            and s_suppkey = ps_suppkey
            and p_size = 25
            and p_type like '%STEEL'
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and r_name = 'EUROPE'
            and ps_supplycost = (
                select
                    min(ps_supplycost)
                from
                    partsupp,
                    supplier,
                    nation,
                    region
                where
                    p_partkey = ps_partkey
                    and s_suppkey = ps_suppkey
                    and s_nationkey = n_nationkey
                    and n_regionkey = r_regionkey
                    and r_name = 'EUROPE'
            )
        order by
            s_acctbal desc,
            n_name,
            s_name,
            p_partkey
        LIMIT 1;
    ''',
    "q3": '''
        select
            l_orderkey,
            sum(l_extendedprice * (1 - l_discount)) as revenue,
            o_orderdate,
            o_shippriority
        from
            customer,
            orders,
            lineitem
        where
            c_mktsegment = 'HOUSEHOLD'
            and c_custkey = o_custkey
            and l_orderkey = o_orderkey
            and o_orderdate < date '1995-03-21'
            and l_shipdate > date '1995-03-21'
        group by
            l_orderkey,
            o_orderdate,
            o_shippriority
        order by
            revenue desc,
            o_orderdate
        limit 10;
    ''',
    "q4": '''
        select
            o_orderpriority,
            count(*) as order_count
        from
            orders
        where
            o_orderdate >= date '1996-03-01'
            and o_orderdate < date '1996-03-01' + interval '3' month
            and exists (
                select
                    *
                from
                    lineitem
                where
                    l_orderkey = o_orderkey
                    and l_commitdate < l_receiptdate
            )
        group by
            o_orderpriority
        order by
            o_orderpriority
        limit 1;
    ''',
    "q5": '''
        select
            n_name,
            sum(l_extendedprice * (1 - l_discount)) as revenue
        from
            customer,
            orders,
            lineitem,
            supplier,
            nation,
            region
        where
            c_custkey = o_custkey
            and l_orderkey = o_orderkey
            and l_suppkey = s_suppkey
            and c_nationkey = s_nationkey
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and r_name = 'AMERICA'
            and o_orderdate >= date '1995-01-01'
            and o_orderdate < date '1995-01-01' + interval '1' year
        group by
            n_name
        order by
            revenue desc
        limit 1;
    ''',
    "q6": '''
        select
            sum(l_extendedprice * l_discount) as revenue
        from
            lineitem
        where
            l_shipdate >= date '1995-01-01'
            and l_shipdate < date '1995-01-01' + interval '1' year
            and l_discount between 0.09 - 0.01 and 0.09 + 0.01
            and l_quantity < 24
        limit 1;
	''',
    "q7": '''
        select
            supp_nation,
            cust_nation,
            l_year,
            sum(volume) as revenue
        from
            (
                select
                    n1.n_name as supp_nation,
                    n2.n_name as cust_nation,
                    extract(year from l_shipdate) as l_year,
                    l_extendedprice * (1 - l_discount) as volume
                from
                    supplier,
                    lineitem,
                    orders,
                    customer,
                    nation n1,
                    nation n2
                where
                    s_suppkey = l_suppkey
                    and o_orderkey = l_orderkey
                    and c_custkey = o_custkey
                    and s_nationkey = n1.n_nationkey
                    and c_nationkey = n2.n_nationkey
                    and (
                        (n1.n_name = 'RUSSIA' and n2.n_name = 'INDIA')
                        or (n1.n_name = 'INDIA' and n2.n_name = 'RUSSIA')
                    )
                    and l_shipdate between date '1995-01-01' and date '1996-12-31'
            ) as shipping
        group by
            supp_nation,
            cust_nation,
            l_year
        order by
            supp_nation,
            cust_nation,
            l_year
        limit 1;
    ''',
    "q8": '''
        select
            o_year,
            sum(case
                when nation = 'UNITED KINGDOM' then volume
                else 0
            end) / sum(volume) as mkt_share
        from
            (
                select
                    extract(year from o_orderdate) as o_year,
                    l_extendedprice * (1 - l_discount) as volume,
                    n2.n_name as nation
                from
                    part,
                    supplier,
                    lineitem,
                    orders,
                    customer,
                    nation n1,
                    nation n2,
                    region
                where
                    p_partkey = l_partkey
                    and s_suppkey = l_suppkey
                    and l_orderkey = o_orderkey
                    and o_custkey = c_custkey
                    and c_nationkey = n1.n_nationkey
                    and n1.n_regionkey = r_regionkey
                    and r_name = 'EUROPE'
                    and s_nationkey = n2.n_nationkey
                    and o_orderdate between date '1995-01-01' and date '1996-12-31'
                    and p_type = 'PROMO PLATED COPPER'
            ) as all_nations
        group by
            o_year
        order by
            o_year
        limit 1;
    ''',
    "q9": '''
        select
            nation,
            o_year,
            sum(amount) as sum_profit
        from
            (
                select
                    n_name as nation,
                    extract(year from o_orderdate) as o_year,
                    l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
                from
                    part,
                    supplier,
                    lineitem,
                    partsupp,
                    orders,
                    nation
                where
                    s_suppkey = l_suppkey
                    and ps_suppkey = l_suppkey
                    and ps_partkey = l_partkey
                    and p_partkey = l_partkey
                    and o_orderkey = l_orderkey
                    and s_nationkey = n_nationkey
                    and p_name like '%orchid%'
            ) as profit
        group by
            nation,
            o_year
        order by
            nation,
            o_year desc
        limit 1;
    ''',
    "q10": '''
        select
            c_custkey,
            c_name,
            sum(l_extendedprice * (1 - l_discount)) as revenue,
            c_acctbal,
            n_name,
            c_address,
            c_phone,
            c_comment
        from
            customer,
            orders,
            lineitem,
            nation
        where
            c_custkey = o_custkey
            and l_orderkey = o_orderkey
            and o_orderdate >= date '1995-01-01'
            and o_orderdate < date '1995-01-01' + interval '3' month
            and l_returnflag = 'R'
            and c_nationkey = n_nationkey
        group by
            c_custkey,
            c_name,
            c_acctbal,
            c_phone,
            n_name,
            c_address,
            c_comment
        order by
            revenue desc
        limit 1;
    ''',
    "q11": '''
        select
            ps_partkey,
            sum(ps_supplycost * ps_availqty) as value
        from
            partsupp,
            supplier,
            nation
        where
            ps_suppkey = s_suppkey
            and s_nationkey = n_nationkey
            and n_name = 'ETHIOPIA'
        group by
            ps_partkey having
                sum(ps_supplycost * ps_availqty) > (
                    select
                        sum(ps_supplycost * ps_availqty) * 0.0001000000
                    from
                        partsupp,
                        supplier,
                        nation
                    where
                        ps_suppkey = s_suppkey
                        and s_nationkey = n_nationkey
                        and n_name = 'ETHIOPIA'
                )
        order by
            value desc
        limit 1;
    ''',
    "q12": '''
        select
            l_shipmode,
            sum(case
                when o_orderpriority = '1-URGENT'
                    or o_orderpriority = '2-HIGH'
                    then 1
                else 0
            end) as high_line_count,
            sum(case
                when o_orderpriority <> '1-URGENT'
                    and o_orderpriority <> '2-HIGH'
                    then 1
                else 0
            end) as low_line_count
        from
            orders,
            lineitem
        where
            o_orderkey = l_orderkey
            and l_shipmode in ('TRUCK', 'AIR')
            and l_commitdate < l_receiptdate
            and l_shipdate < l_commitdate
            and l_receiptdate >= date '1997-01-01'
            and l_receiptdate < date '1997-01-01' + interval '1' year
        group by
            l_shipmode
        order by
            l_shipmode
        limit 1;
    ''',
    "q13": '''
        select
            c_count,
            count(*) as custdist
        from
            (
                select
                    c_custkey,
                    count(o_orderkey)
                from
                    customer left outer join orders on
                        c_custkey = o_custkey
                        and o_comment not like '%pending%packages%'
                group by
                    c_custkey
            ) as c_orders (c_custkey, c_count)
        group by
            c_count
        order by
            custdist desc,
            c_count desc
        limit 1;
    ''',
    "q14": '''
        select
            100.00 * sum(case
                when p_type like 'PROMO%'
                    then l_extendedprice * (1 - l_discount)
                else 0
            end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
        from
            lineitem,
            part
        where
            l_partkey = p_partkey
            and l_shipdate >= date '1993-11-01'
            and l_shipdate < date '1993-11-01' + interval '1' month
        limit 1;
    ''',
    "q15": '''
        create view REVENUE0 (supplier_no, total_revenue) as select l_suppkey, sum(l_extendedprice * (1 - l_discount)) from LINEITEM where l_shipdate >= date '1997-07-01' and l_shipdate < date '1997-07-01' + interval '3' month group by l_suppkey; 
        select s_suppkey, s_name, s_address, s_phone, total_revenue from SUPPLIER, REVENUE0 where s_suppkey = supplier_no and total_revenue = ( select max(total_revenue) from REVENUE0) order by s_suppkey; 
        drop view REVENUE0;
    ''',
    "q16": '''
        select
            p_brand,
            p_type,
            p_size,
            count(distinct ps_suppkey) as supplier_cnt
        from
            partsupp,
            part
        where
            p_partkey = ps_partkey
            and p_brand <> 'Brand#23'
            and p_type not like 'MEDIUM BRUSHED%'
            and p_size in (45, 35, 7, 23, 24, 18, 14, 15)
            and ps_suppkey not in (
                select
                    s_suppkey
                from
                    supplier
                where
                    s_comment like '%Customer%Complaints%'
            )
        group by
            p_brand,
            p_type,
            p_size
        order by
            supplier_cnt desc,
            p_brand,
            p_type,
            p_size
        limit 1;
    ''',
    "q17": '''
        select
            sum(l_extendedprice) / 7.0 as avg_yearly
        from
            lineitem,
            part,
                (select l_partkey as agg_partkey, 0.2 * avg(l_quantity) as avg_quantity from lineitem group by l_partkey) part_agg
        where
            p_partkey = l_partkey
                and agg_partkey = l_partkey
            and p_brand = 'Brand#33'
            and p_container = 'WRAP JAR'
            and l_quantity < avg_quantity
        limit 1;
    ''',
    "q18": '''
        select
            c_name,
            c_custkey,
            o_orderkey,
            o_orderdate,
            o_totalprice,
            sum(l_quantity)
        from
            customer,
            orders,
            lineitem
        where
            o_orderkey in (
                select
                    l_orderkey
                from
                    lineitem
                group by
                    l_orderkey having
                        sum(l_quantity) > 314
            )
            and c_custkey = o_custkey
            and o_orderkey = l_orderkey
        group by
            c_name,
            c_custkey,
            o_orderkey,
            o_orderdate,
            o_totalprice
        order by
            o_totalprice desc,
            o_orderdate
        limit 1;
    ''',
    "q19": '''
        select
            sum(l_extendedprice* (1 - l_discount)) as revenue
        from
            lineitem,
            part
        where
            (
                p_partkey = l_partkey
                and p_brand = 'Brand#54'
                and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
                and l_quantity >= 4 and l_quantity <= 4 + 10
                and p_size between 1 and 5
                and l_shipmode in ('AIR', 'AIR REG')
                and l_shipinstruct = 'DELIVER IN PERSON'
            )
            or
            (
                p_partkey = l_partkey
                and p_brand = 'Brand#51'
                and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
                and l_quantity >= 11 and l_quantity <= 11 + 10
                and p_size between 1 and 10
                and l_shipmode in ('AIR', 'AIR REG')
                and l_shipinstruct = 'DELIVER IN PERSON'
            )
            or
            (
                p_partkey = l_partkey
                and p_brand = 'Brand#21'
                and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
                and l_quantity >= 28 and l_quantity <= 28 + 10
                and p_size between 1 and 15
                and l_shipmode in ('AIR', 'AIR REG')
                and l_shipinstruct = 'DELIVER IN PERSON'
            )
        limit 1;
    ''',
    "q20": '''select
                s_name,
                s_address
            from
                supplier,
                nation
            where
                s_suppkey in (
                    select
                        ps_suppkey
                    from
                        partsupp,
                        (
                            select
                                l_partkey agg_partkey,
                                l_suppkey agg_suppkey,
                                0.5 * sum(l_quantity) AS agg_quantity
                            from
                                lineitem
                            where
                                l_shipdate >= date '1997-01-01'
                                and l_shipdate < date '1997-01-01' + interval '1' year
                            group by
                                l_partkey,
                                l_suppkey
                        ) agg_lineitem
                    where
                        agg_partkey = ps_partkey
                        and agg_suppkey = ps_suppkey
                        and ps_partkey in (
                            select
                                p_partkey
                            from
                                part
                            where
                                p_name like 'powder%'
                        )
                        and ps_availqty > agg_quantity
                )
                and s_nationkey = n_nationkey
                and n_name = 'ARGENTINA'
            order by
                s_name
            limit 1;''',
    "q21": '''
        select
            s_name,
            count(*) as numwait
        from
            supplier,
            lineitem l1,
            orders,
            nation
        where
            s_suppkey = l1.l_suppkey
            and o_orderkey = l1.l_orderkey
            and o_orderstatus = 'F'
            and l1.l_receiptdate > l1.l_commitdate
            and exists (
                select
                    *
                from
                    lineitem l2
                where
                    l2.l_orderkey = l1.l_orderkey
                    and l2.l_suppkey <> l1.l_suppkey
            )
            and not exists (
                select
                    *
                from
                    lineitem l3
                where
                    l3.l_orderkey = l1.l_orderkey
                    and l3.l_suppkey <> l1.l_suppkey
                    and l3.l_receiptdate > l3.l_commitdate
            )
            and s_nationkey = n_nationkey
            and n_name = 'BRAZIL'
        group by
            s_name
        order by
            numwait desc,
            s_name
        limit 1;
    ''',
    "q22": '''
        select
            cntrycode,
            count(*) as numcust,
            sum(c_acctbal) as totacctbal
        from
            (
                select
                    substring(c_phone from 1 for 2) as cntrycode,
                    c_acctbal
                from
                    customer
                where
                    substring(c_phone from 1 for 2) in
                        ('20', '10', '18', '16', '17', '29', '21')
                    and c_acctbal > (
                        select
                            avg(c_acctbal)
                        from
                            customer
                        where
                            c_acctbal > 0.00
                            and substring(c_phone from 1 for 2) in
                                ('20', '10', '18', '16', '17', '29', '21')
                    )
                    and not exists (
                        select
                            *
                        from
                            orders
                        where
                            o_custkey = c_custkey
                    )
            ) as custsale
        group by
            cntrycode
        order by
            cntrycode;
    '''
}

cardinality_info = {
    "CUSTOMER": 150000,
    "ORDERS": 1500000,
    "LINEITEM": 6001215,
    "NATION": 25,
    "PARTSUPP": 800000,
    "PART": 200000,
    "REGION": 5,
    "SUPPLIER": 10000
}

timeout=11

light_reward_scale=10
heavy_reward_scale=10