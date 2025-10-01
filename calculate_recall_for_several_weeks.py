import pandas as pd
import numpy as np

def calculate_recall(ground_truth, top_products, user_candidates, strategy="past_history"):
    hits = 0
    total = 0
    recalls = []

    for user, target_items in ground_truth.items():
        if strategy == 'past_history':
            candidate_items = user_candidates.get(user, top_products)  # if no purchases, use top
        elif strategy == 'top':
            candidate_items = top_products
        else:
            raise ValueError("Unknown strategy")

        target_set = set(target_items)
        candidate_set = set(candidate_items)

        overlap = len(target_set & candidate_set)

        hits += overlap
        total += len(target_set)

        recalls.append(overlap / len(target_set) if len(target_set) > 0 else 0)

    recall_macro = np.mean(recalls)        # avg across users (user-level Recall)
    recall_micro = hits / total if total > 0 else 0   # global Recall (item-level Recall)
    return recall_macro, recall_micro

def calculate_for_week(train, test, ground_truth,strategy):

    end_date = train['t_dat'].max()
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=30)

    window_df = train[(train['t_dat'] >= start_date) & (train['t_dat'] <= end_date)]

    top_products = window_df['article_id'].value_counts().head(1000).index.tolist() # NOt IN Train
   

    lookup_set = set(test['customer_id'].tolist())
    test_customers_in_train = train[train['customer_id'].isin(lookup_set)].copy()

    user_previous_purchases = (test_customers_in_train.groupby("customer_id")["article_id"].unique().to_dict())

    #user_candidates = {}

    #for user, purchases in user_previous_purchases.items():
    #    candidates = set(purchases)
    #    candidates.update(top_products)
    #    user_candidates[user] = list(candidates)


    _, recall = calculate_recall(ground_truth,top_products, user_previous_purchases, strategy) 
    return recall
    
    
def calculate_for_several_weeks(df):
    #window 
    #train_set
    #val_set
    #true_val

    results = []
    weeks = sorted(df["week"].unique())

    #w = '2020-09-16/2020-09-22'

    for i, week in enumerate(weeks[98:105]): 
        print(i)
        #week = w
        test = df[df['week']== week]
        #print('test week: ', test['t_dat'].min(), test['t_dat'].max())
        train = df[(df['week']< week)] 
        #print('train date:', train['t_dat'].min(), train['t_dat'].max())

        ground_truth = test.groupby('customer_id')['article_id'].apply(set).to_dict()

        

        # baseline_preds и new_preds (for train)
        # baseline = Global top from train
        # Rebuild window for a top products. 
        recall_baseline = calculate_for_week(df, train, test, ground_truth,strategy='popular')
        recall_popular = calculate_for_week(df, train, test, ground_truth,strategy='past_history')


        results.append({
            "week": str(week),
            "baseline": recall_baseline,
            "new": recall_popular
        })

    results_df = pd.DataFrame(results)
    return results_df
