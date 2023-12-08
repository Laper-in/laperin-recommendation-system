import sys
from db_access import DatabaseAccess
from text_preprocessing import TextPreprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self):
        self.db_acc = DatabaseAccess()
        self.txt_prep = TextPreprocessing()
        self.table = 'recipe_ingredients'

    def recommend_recipes(self, user_ingredients):
        recipe_ids = self.db_acc.read_id(self.table)
        ingredients = self.db_acc.read_ingredients(self.table)

        recipe_ids_ls = self.txt_prep.sql_query_to_list(recipe_ids)
        ingredients_ls = self.txt_prep.sql_query_to_list(ingredients)

        docs = self.txt_prep.combine_query_content(user_ingredients, ingredients_ls)

        vectorizer = TfidfVectorizer(smooth_idf=False, norm=None)
        docs_weight = vectorizer.fit_transform(docs)
        query_weight = vectorizer.transform([user_ingredients])
        cos_sim = cosine_similarity(query_weight, docs_weight).flatten()

        cos_sim = cos_sim[1:]
        cos_sim_dict = dict(enumerate(cos_sim))
        cos_sim_dict = {k: v for k, v in sorted(cos_sim_dict.items(), key=lambda item: item[1], reverse=True) if v > 0.4}

        idx_for_id = list(cos_sim_dict.keys())
        recipe_ids_rank = [recipe_ids_ls[i] for i in idx_for_id]

        return recipe_ids_rank

if __name__ == "__main__":
    if len(sys.argv) == 2:
        user_input = sys.argv[1]
        recommender = Recommender()
        recommended_recipes = recommender.recommend_recipes(user_input)
        sys.stdout.write(', '.join(map(str, recommended_recipes)))
    else:
        print("Please provide user ingredients.")