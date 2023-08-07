import logging
import requests
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from typing import List
from pyalex import Works, Authors

class OpenAlexAuthorsReader(BaseReader):
    """
    A class to read and process data from OpenAlex
    ...

    Methods
    -------
    __init__():
       Instantiate the OpenAlex object
    """

    def __init__(self):
        """
        Instantiate the OpenAlex object
        """
        self.a = Authors()
        self.w = Works()

    def load_data(
        self,
        query,
        limit=10,
        returned_fields=[
            "display_name",
            "last_known_institution",
            "works"
        ],
    ) -> List[Document]:
        """
        Loads data from Semantic Scholar based on the entered query and returned_fields

        Parameters
        ----------
        query: str
            The search query for the paper
        limit: int, optional
            The number of maximum results returned (default is 10)
        returned_fields: list, optional
            The list of fields to be returned from the search

        Returns
        -------
        list
            The list of Document object that contains the search results

        Raises
        ------
        Exception
            If there is an error while performing the search

        """
        try:
            results = self.a.search_filter(display_name=query).get()
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logging.error(
                "Failed to fetch data from OpenAlex with exception: %s", e
            )
            raise
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            raise

        documents = []
        for item in results[:limit]:
            openalexauthorid = item["id"].split('/')[-1]
            display_name = item["display_name"]
            print(item["last_known_institution"])
            last_known_institution = ''
            try:
                last_known_institution = item["last_known_institution"]["display_name"]
            except Exception as err:
                pass
            cited_by_count = item["cited_by_count"]
            works = self.w.filter(author={"id": openalexauthorid}).get()
            for work in works:
                text = ''
                abstract = ''
                title = work["title"]
                try:
                    abstract = work["abstract"]
                except Exception as err:
                    abstract = ''
                # concat title and abstract
                if abstract and title:
                    text = title + " " + abstract
                elif not abstract:
                    text = title
                venue = ''
                try:
                    venue = work["primary_location"]["source"]["display_name"]
                except Exception as err:
                    venue = ''
                metadata = {
                    "title": title,
                    "author": display_name,
                    "last_known_institution":last_known_institution,
                    "cited_by_count":cited_by_count,
                    "authors": [author["author"]["display_name"] for author in work["authorships"]],
                    "venue": venue
                }
                documents.append(Document(text=text, extra_info=metadata))
        return documents
class OpenAlexWorksReader(BaseReader):
    """
    A class to read and process data from OpenAlex
    ...

    Methods
    -------
    __init__():
       Instantiate the OpenAlex object
    """

    def __init__(self):
        """
        Instantiate the OpenAlex object
        """
        self.w = Works()

    def load_data(
        self,
        query,
        limit=10,
        returned_fields=[
            "title",
            "authors",
            "venue"
        ],
    ) -> List[Document]:
        """
        Loads data from Semantic Scholar based on the entered query and returned_fields

        Parameters
        ----------
        query: str
            The search query for the paper
        limit: int, optional
            The number of maximum results returned (default is 10)
        returned_fields: list, optional
            The list of fields to be returned from the search

        Returns
        -------
        list
            The list of Document object that contains the search results

        Raises
        ------
        Exception
            If there is an error while performing the search

        """
        try:
            results = self.w.search(query).get()
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logging.error(
                "Failed to fetch data from OpenAlex with exception: %s", e
            )
            raise
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            raise

        documents = []
        for item in results[:limit]:
            title = item["title"]
            text = None
            openalexid = item['id'].split('/')[-1]
            work = self.w[openalexid]
            abstract = ''
            try:
                abstract = work["abstract"]
            except Exception as err:
                abstract = ''
            # concat title and abstract
            if abstract and title:
                text = title + " " + abstract
            elif not abstract:
                text = title
            venue = ''
            try:
                venue = work["primary_location"]["source"]["display_name"]
            except Exception as err:
                venue = ''
            metadata = {
                "title": title,
                "authors": [author["author"]["display_name"] for author in work["authorships"]],
                "venue": venue
            }
            documents.append(Document(text=text, extra_info=metadata))
        return documents
