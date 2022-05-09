import numpy as np
import pandas as pd
import matplotli.pyplot as plt
import missingno
import seaborn as sns
import math

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from sklearn import model_selection, svm

from sklearn.tree import export_graphviz
import graphviz

data_df = pd.read_csv('pre_credit_df(fill_groupby).csv', index_col=0)

X=data_df.drop('credit', axis=1)
y=data_df[['credit']]

def run_pipeline(X, y):
    #자동으로 num과 cat 변수 갈라서 df 생성
    X_cat = X.select_dtypes(include=np.object)
    X_num = X.select_dtypes(exclude=np.object)

    # binary df 만들어주기 = pass through 위해 id도 여기 넣어주기
    X_bi = X[['gender','car','reality','work_phone','phone','email','id']]

    # cat인데 num df에 들어간 변수 num df에서 drop해주기
    X_num = X_num.drop(columns=['id','gender','car','reality','work_phone','phone','email'])

    x_train, x_test, y_train, y_test = train_test_split(X,
                                                                    y,
                                                                   test_size = 0.2,
                                                                   random_state=0)
    
    binary_features = X_bi.columns
    
    numeric_features = X_num.columns
    numeric_transformer = StandardScaler() # cf) RobustScaler

    categorical_features = X_cat.columns
    categorical_transformer = OneHotEncoder(categories='auto', handle_unknown='ignore') # categories='auto' : just for ignoring warning messages

    preprocessor = ColumnTransformer(
        transformers=[ # List of (name, transformer, column(s))
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features),
             ('bi','passthrough',binary_features)])

    preprocessor_pipe = Pipeline(steps=[('preprocessor', preprocessor)])
    preprocessor_pipe.fit(x_train)

    x_train_transformed = preprocessor_pipe.transform(x_train)
    x_test_transformed = preprocessor_pipe.transform(x_test)

    return x_train_transformed, x_test_transformed, y_train, y_test, preprocessor
  
x_train_transformed, x_test_transformed, y_train, y_test, preprocessor = run_pipeline(X, y)
  
model = DecisionTreeClassifier(max_depth=5)
model.fit(x_train_transformed,y_train)
model.score(x_test_transformed,y_test) #logloss로 뽑아보기

def get_feature_names(column_transformer):

    def get_names(trans):
        # >> Original get_feature_names() method
        if trans == 'drop' or (
                hasattr(column, '__len__') and not len(column)):
            return []
        if trans == 'passthrough':
            if hasattr(column_transformer, '_df_columns'):
                if ((not isinstance(column, slice))
                        and all(isinstance(col, str) for col in column)):
                    return column
                else:
                    return column_transformer._df_columns[column]
            else:
                indices = np.arange(column_transformer._n_features)
                return ['x%d' % i for i in indices[column]]
        if not hasattr(trans, 'get_feature_names'):
        # >>> Change: Return input column names if no method avaiable
            # Turn error into a warning
            warnings.warn("Transformer %s (type %s) does not "
                                 "provide get_feature_names. "
                                 "Will return input column names if available"
                                 % (str(name), type(trans).__name__))
            # For transformers without a get_features_names method, use the input
            # names to the column transformer
            if column is None:
                return []
            else:
                return [name + "__" + f for f in column]

        return [name + "__" + f for f in trans.get_feature_names()]
    
    ### Start of processing
    feature_names = []
    
    # Allow transformers to be pipelines. Pipeline steps are named differently, so preprocessing is needed
    if type(column_transformer) == Pipeline:
        l_transformers = [(name, trans, None, None) for step, name, trans in column_transformer._iter()]
    else:
        # For column transformers, follow the original method
        l_transformers = list(column_transformer._iter(fitted=True))
    
    
    for name, trans, column, _ in l_transformers: 
        if type(trans) == Pipeline:
            # Recursive call on pipeline
            _names = get_feature_names(trans)
            # if pipeline has no transformer that returns names
            if len(_names)==0:
                _names = [name + "__" + f for f in column]
            feature_names.extend(_names)
        else:
            feature_names.extend(get_names(trans))
    
    return feature_names
  
new_col_names = get_feature_names(preprocessor)
x_train_transformed = pd.DataFrame(x_train_transformed,columns=new_col_names)
x_test_transformed = pd.DataFrame(x_test_transformed,columns=new_col_names)

dot_data = export_graphviz(model,   # 의사결정나무 모형 대입
                           out_file = None,  # file로 변환할 것인가
                           feature_names = x_train_transformed.columns,  # feature 이름
                           class_names = None,  # target 이름
                           filled = True,           # 그림에 색상사용 여부
                           rounded = True,          # 반올림을 진행 여부
                           special_characters = True)   # 특수문자를 사용여부

graph = graphviz.Source(dot_data)              


graph.render(filename='tree1.pdf')




  
