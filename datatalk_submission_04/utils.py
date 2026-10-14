from sklearn.model_selection import train_test_split


def split_dataset(df, target, test_size=0.2, val_size=None, random_state=42):
    """Split a DataFrame into train/test (and optionally validation) sets.

    Sizes are fractions of the full dataset, e.g. test_size=0.2, val_size=0.2
    gives a 60/20/20 split.

    Returns (X_train, X_test, y_train, y_test), or
    (X_train, X_val, X_test, y_train, y_val, y_test) when val_size is set.
    """
    df_full_train, df_test = train_test_split(
        df, test_size=test_size, random_state=random_state
    )

    if val_size:
        # rescale val_size so it is a fraction of the full dataset, not of df_full_train
        df_train, df_val = train_test_split(
            df_full_train,
            test_size=val_size / (1 - test_size),
            random_state=random_state,
        )
        splits = [df_train, df_val, df_test]
    else:
        splits = [df_full_train, df_test]

    splits = [d.reset_index(drop=True) for d in splits]
    X = [d.drop(columns=[target]) for d in splits]
    y = [d[target].values for d in splits]
    return (*X, *y)
