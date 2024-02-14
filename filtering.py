import pandas as pd

# Dictionary containing positive and negative sentiment words
sentimentWords = {
    'positive': ["amazing", "awesome", "brilliant", "fantastic", "excellent", "fabulous", "wonderful", "perfect", "incredible",
                 "exceptional", "positive", "delightful", "pleasing", "enjoyable", "spectacular", "magnificent", "marvelous",
                 "outstanding", "superb", "great", "happy", "joyful", "lovely", "charming", "cheerful", "satisfying", "gratifying",
                 "beautiful", "elegant", "exquisite", "gorgeous", "fine", "radiant", "splendid", "stunning", "admirable", "glorious",
                 "pretty", "nice", "pleasant", "agreeable", "breathtaking", "heartwarming", "inspiring", "uplifting", "thrilling",
                 "successful", "victorious", "profitable", "beneficial"],
    'negative': ["awful", "terrible", "horrible", "dreadful", "poor", "bad", "worse", "worst", "unpleasant", "disappointing",
                 "unsatisfactory", "lamentable", "deplorable", "atrocious", "appalling", "dismal", "depressing", "dire", "gloomy",
                 "sad", "unhappy", "miserable", "sorrowful", "melancholy", "grief-stricken", "heartbroken", "anguished", "distressing",
                 "painful", "tragic", "harmful", "damaging", "destructive", "injurious", "pernicious", "fatal", "deadly", "lethal",
                 "noxious", "detrimental", "negative", "disadvantageous", "unfavorable", "adverse", "hateful", "hostile", "resentful",
                 "bitter", "angry", "irate", "outraged"]
}


def sort_reviews(reviews, by):
    """
    Function to sort reviews based on different criteria.

    Parameters:
    reviews (DataFrame): The reviews dataframe.
    by (str): The criteria to sort by. Can be 'Score', 'Review Text', 'No Text', 'Sentiment', or any other column name.

    Returns:
    DataFrame: The sorted reviews dataframe.
    """
    # Sort by score
    if by == 'score':
        return reviews.sort_values(by='Score', ascending=False)
    # Sort by review text
    elif by == 'text':
        return reviews[reviews['Review Text'].notnull()].sort_values(by='Date', ascending=False)
    # Sort by no text
    elif by == 'no-text':
        return reviews[reviews['Review Text'].isnull()].sort_values(by='Date', ascending=False)
    # Sort by sentiment
    elif by == 'positive' or by == 'negative' or by == 'neutral':
        # Convert score to numeric
        reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
        # Filter by positive sentiment
        if by == 'positive':
            filtered_reviews = reviews[
                (reviews['Review Text'].str.contains('|'.join(sentimentWords[by]), na=False)) &
                (reviews['Score'] >= 4)
                ]
        # Filter by negative sentiment
        elif by == 'negative':
            filtered_reviews = reviews[
                (reviews['Review Text'].str.contains('|'.join(sentimentWords[by]), na=False)) &
                (reviews['Score'] <= 2)
                ]
        # Filter by neutral sentiment
        else:
            filtered_reviews = reviews[reviews['Score'] == 3]
        return filtered_reviews.sort_values(by='Date', ascending=False)
    # Default sort by date
    else:
        return reviews.sort_values(by='Date', ascending=False)
