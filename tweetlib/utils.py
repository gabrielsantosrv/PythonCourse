import re

def filter_tweets(df, df_b3_shares, return_df=False):
    '''

    :param df: pandas.DataFrame containing column 'text'
    :param df_b3_shares: pandas.DataFrame with B3 companies data
    :param return_df: flag indicating whether return a pandas.DataFrame or not
    :return: a list or pandas.DataFrame (depending on return_df flag) with the filtered tweets
    '''
    codes = df_b3_shares[(df_b3_shares['CÓDIGO'] != 'LEVE') &
                         (df_b3_shares['CÓDIGO'] != 'QUAL') &
                         (df_b3_shares['CÓDIGO'] != 'CEDO') &
                         (df_b3_shares['CÓDIGO'] != 'VIVA') &
                         (df_b3_shares['CÓDIGO'] != 'NORD') &
                         (df_b3_shares['CÓDIGO'] != 'SHOW') &
                         (df_b3_shares['CÓDIGO'] != 'ALSO') &
                         (df_b3_shares['CÓDIGO'] != 'AGRO') &
                         (df_b3_shares['CÓDIGO'] != 'RAIL') &
                         (df_b3_shares['CÓDIGO'] != 'VALE')]['CÓDIGO']

    # Select by stock code
    code = '|'.join(codes)
    digit = '|'.join([str(x) for x in range(1, 12)])

    pattern = '(^|\W)({})({})?($|\W)'.format(code, digit)

    if return_df:
        df_tweets = df[df['text'].str.contains(pattern, regex=True, case=False)]
    else:
        tweets = list(df['text'][df['text'].str.contains(pattern, regex=True, case=False)])

    pattern = '(^|\W)(LEVE|QUAL|CEDO|VIVA|NORD|SHOW|ALSO|AGRO|RAIL)({})($|\W)'.format(digit)

    if return_df:
        df_tweets = df_tweets.append(df[df['text'].str.contains(pattern, regex=True, case=False)], ignore_index=True)
    else:
        tweets.extend(df['text'][df['text'].str.contains(pattern, regex=True, case=False)])

    pattern = '(^|\W)(VALE)({})?($|\W)'.format(digit)

    if return_df:
        df_tweets = df_tweets.append(df[(df['text'].str.contains(pattern, regex=True, case=False)) &
                                        ~(df['text'].str.contains('vale\s+a\s+pena', regex=True, case=False))],
                                     ignore_index=True)
    else:
        tweets.extend(df['text'][(df['text'].str.contains(pattern, regex=True, case=False)) &
                                 ~(df['text'].str.contains('vale\s+a\s+pena', regex=True, case=False))])

    # Select by company name

    # remove SA in the names
    company_names = [re.sub(r'\sS(/|\.)?A\.?$', '', text, re.IGNORECASE) for text in df_b3_shares['NOME DA EMPRESA']
                     if text not in ['VALE', 'B3', 'LIGHT', 'LIGHT S/A', 'OI', 'RUMO', 'ECON', 'VIVER', 'Mundial']]
    company_names.extend(['LIGHT S/A', 'OI S/A', 'RUMO S/A', 'ECON S/A', 'VIVER S/A', 'Mundial S/A'])

    pattern = '(^|\W)({})($|\W)'.format('|'.join(company_names))

    if return_df:
        df_tweets = df_tweets.append(df[df['text'].str.contains(pattern, regex=True, case=False)], ignore_index=True)
    else:
        tweets.extend(df['text'][df['text'].str.contains(pattern, regex=True, case=False)])

    if return_df:
        return df_tweets.drop_duplicates(subset=['id'])

    return tweets