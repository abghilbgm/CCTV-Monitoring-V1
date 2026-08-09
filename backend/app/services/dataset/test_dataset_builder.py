from app.services.dataset.dataset_builder import DatasetBuilder
from app.services.dataset.splitter import DatasetSplitter

def main():
    splitter = DatasetSplitter()
    splits = splitter.split()

    builder = DatasetBuilder()
    builder.build(splits)

if __name__ == "__main__":
    main()
