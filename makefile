
data/data_features.csv: make_data.py config/config.yml
	python make_data.py --config=config/config.yml --output=data/data_features.csv

data/model.pkl: data/data_features.csv train_model.py config/config.yml
	python train_model.py --config=config/config.yml --input=data/data_features.csv --output=data/model.pkl

make_data: data/data_features.csv

train_model: data/model.pkl

all: make_data train_model

