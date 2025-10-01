def map_at_k(ground_truth, user_candidates, k=12):

    average_precisions = []
    
    for user, target_items in ground_truth.items():
        #candidate_items = user_candidates.get(user, top_products)
        candidate_items = (user_candidates[user_candidates['customer_id']==user]['predictions']).values[0]
    
        score = 0.0
        hits = 0
    
        for i, p in enumerate(candidate_items):
            if p in target_items:
                hits += 1
                score += hits / (i + 1)
            #print(hits)
    
        if target_items:
            average_precisions.append(score / min(len(target_items), k))
        else:
            average_precisions.append(0.0)
    #print('average_precisions=', average_precisions, 'len(average_precisions) ', len(average_precisions))
        

    return sum(average_precisions) / len(average_precisions)
