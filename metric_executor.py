# def execute_metric(df, metric_spec, group_by=None):

#     name = metric_spec.name

#     if name == "revenue":
#         df_filtered = df[df["Status"] != "Cancelled"]

#         if group_by:
#             return df_filtered.groupby(group_by)["Amount"].sum()

#         return df_filtered["Amount"].sum()

#     elif name == "order_count":
#         if group_by:
#             return df.groupby(group_by)["Order ID"].nunique()

#         return df["Order ID"].nunique()

#     elif name == "units_sold":
#         if group_by:
#             return df.groupby(group_by)["Qty"].sum()

#         return df["Qty"].sum()

#     # add more...

#     return None
def execute_metric(df, metric_spec, group_by=None):

    name = metric_spec.name

    if name == "revenue":
        df = df[df["Status"] != "Cancelled"]

        if group_by:
            return df.groupby(group_by)["Amount"].sum().reset_index()

        return df["Amount"].sum()

    elif name == "order_count":
        if group_by:
            return df.groupby(group_by)["Order ID"].nunique().reset_index()

        return df["Order ID"].nunique()

    elif name == "units_sold":
        if group_by:
            return df.groupby(group_by)["Qty"].sum().reset_index()

        return df["Qty"].sum()

    return None