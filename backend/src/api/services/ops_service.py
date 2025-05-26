import requests
import base64

from api.config.ops_config import ops_api_url, ops_consumer_key, ops_consumer_secret_key


def get_access_token(api_url: str, consumer_key: str, consumer_secret_key: str) -> str:
    """Get access token from Ops API.

    Args:
        api_url (str): The Ops API URL.
        consumer_key (str): The consumer key for authentication.
        consumer_secret_key (str): The consumer secret key for authentication.
    Returns:
        str: The access token.
    Raises:
        Exception: If the request fails or the access token is not found.
    """

    # Encode the consumer key and secret key in base64
    base_64_encoded = base64.b64encode(
        bytes(f"{consumer_key}:{consumer_secret_key}", 'utf-8')).decode('utf-8')

    url = f"{api_url}/auth/accesstoken"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base_64_encoded}'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    try:
        # Make the request to get the access token
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the access token from the response
        access_token = response.json().get('access_token')
        if not access_token:
            raise ValueError("Access token not found in the response.")

        return access_token

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")


def get_patent_description(api_url: str, access_token: str, type: str = "publication", format: str = "epodoc", number: str = "EP1000000") -> list[str]:
    """Get patent data from Ops API.

    Args:
        api_url (str): The Ops API URL.
        access_token (str): The access token for authentication.
        type (str): Reference type (application, priority, publication).
        format (str): The format of the patent data (docdb, epodoc).
        number (str): The patent number.
    Returns:
        list[str]: The patent data in the specified format.
    Raises:
        Exception: If the request fails or the patent data is not found.
    """

    url = f"{api_url}/rest-services/published-data/{type}/{format}/{number}/description"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    try:
        # Make the request to get the patent data
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the patent data from the response
        patent_data = response.json()
        if not patent_data:
            raise ValueError("Patent data not found in the response.")

        # Extract only the description from the patent data
        description_data = patent_data.get("ops:world-patent-data", {}).get("ftxt:fulltext-documents", {
        }).get("ftxt:fulltext-document", {}).get("description", {}).get("p", [])

        # Ensure the description is a list of strings
        if isinstance(description_data, dict):
            description_data = [description_data]

        description = [p["$"] for p in description_data if "$" in p]

        if not description:
            raise ValueError("Description not found in the response.")

        return description

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected response structure: {e}")


def get_patent_claims(api_url: str, access_token: str, type: str = "publication", format: str = "epodoc", number: str = "EP1000000") -> list[str]:
    """Get patent claims from Ops API.

    Args:
        api_url (str): The Ops API URL.
        access_token (str): The access token for authentication.
        type (str): Reference type (application, priority, publication).
        format (str): The format of the patent data (docdb, epodoc).
        number (str): The patent number.
    Returns:
        list[str]: A list of patent claims in the specified format.
    Raises:
        Exception: If the request fails or the patent claims are not found.
    """

    url = f"{api_url}/rest-services/published-data/{type}/{format}/{number}/claims"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    try:
        # Make the request to get the patent claims
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the patent claims from the response
        patent_data = response.json()
        if not patent_data:
            raise ValueError("Patent data not found in the response.")

        # Extract only the claims from the patent data
        claims_data = patent_data.get("ops:world-patent-data", {}).get("ftxt:fulltext-documents", {}).get(
            "ftxt:fulltext-document", {}).get("claims", {}).get("claim", {}).get("claim-text", [])

        # Ensure claims_data is a list
        if isinstance(claims_data, dict):  # Single claim case
            claims_data = [claims_data]

        # Extract the claim text
        claims_text = [claim.get("$", "") for claim in claims_data]

        if not claims_text:
            raise ValueError("No claims found in the response.")

        return claims_text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected response structure: {e}")


def get_patent_biblio(api_url: str, access_token: str, type: str = "publication", format: str = "epodoc", number: str = "EP1000000") -> dict:
    """Get patent bibliographic data from Ops API.

    Args:
        api_url (str): The Ops API URL.
        access_token (str): The access token for authentication.
        type (str): Reference type (application, priority, publication).
        format (str): The format of the patent data (docdb, epodoc).
        number (str): The patent number.
    Returns:
        dict: The patent bibliographic data in the specified format.
    """
    url = f"{api_url}/rest-services/published-data/{type}/{format}/{number}/biblio"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    try:
        # Make the request to get the patent bibliographic data
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the bibliographic data from the response
        patent_data = response.json()
        if not patent_data:
            raise ValueError("Patent data not found in the response.")

        exchange_documents = patent_data.get(
            "ops:world-patent-data", {}).get("exchange-documents", {}).get("exchange-document", [])
        if isinstance(exchange_documents, dict):
            exchange_documents = [exchange_documents]
        first_exchange_document = exchange_documents[0]

        # Extract the publication date
        publication_reference = first_exchange_document.get(
            "bibliographic-data", {}).get("publication-reference", {}).get("document-id", [])
        if isinstance(publication_reference, dict):
            publication_reference = [publication_reference]

        publication_date = None
        for doc_id in publication_reference:
            if doc_id.get("@document-id-type") == "docdb":
                publication_date = doc_id.get("date", {}).get("$")
                break

        # Extract the patent titles
        invention_titles = first_exchange_document.get(
            "bibliographic-data", {}).get("invention-title", [])
        titles = {}
        if invention_titles:
            for title in invention_titles:
                lang = title.get("@lang")
                title_text = title.get("$")
                if lang and title_text:
                    titles[lang] = title_text

        # Extract abstracts
        result_abstracts = first_exchange_document.get("abstract", [])
        if isinstance(result_abstracts, dict):
            result_abstracts = [result_abstracts]
        abstracts = {}
        if result_abstracts:
            for abstract in result_abstracts:
                lang = abstract.get("@lang")
                abstract_text = abstract.get("p", {}).get("$")
                if lang and abstract_text:
                    abstracts[lang] = abstract_text

        return {
            "number": number,
            "title": titles,
            "abstract": abstracts,
            "publication_date": publication_date
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected response structure: {e}")


def get_full_patent(api_url: str, consumer_key: str, consumer_secret_key: str, patent_number: str) -> list[dict]:
    """Get patents from Ops API based on the given date and type.
    Args:
        api_url (str): The Ops API URL.
        consumer_key (str): The consumer key for authentication.
        consumer_secret_key (str): The consumer secret key for authentication.
        query (str): The search query for patents in CQL language.
    Returns:
        list[dict]: A list of patents with detailed information.
    """

    # Get the access token
    access_token = get_access_token(api_url, consumer_key, consumer_secret_key)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    patent = {}

    # Construct the URL for the patent search
    url = f"{api_url}/rest-services/published-data/search?Range=1-1&q=pn = {patent_number}"

    # Make the request to get the patents matching the criteria
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    # Extract the patents from the response
    patent_data = response.json()
    if not patent_data:
        raise ValueError("Patent data not found in the response.")

    # Extract publication references
    publications = patent_data.get("ops:world-patent-data", {}).get(
        "ops:biblio-search", {}).get("ops:search-result", {}).get("ops:publication-reference", [])

    if isinstance(publications, dict):
        publications = [publications]

    # Process each publication
    for publication in publications:
        number = None

        try:
            document_id = publication.get("document-id", {})
            doc_number = document_id.get(
                "doc-number", {}).get("$", "")
            format = document_id.get("@document-id-type", "")
            kind = document_id.get("kind", {}).get("$", "")
            country = document_id.get("country", {}).get("$", "")
            number = f"{country}{doc_number}{kind}"

            # Fetch detailed data for each patent
            biblio = get_patent_biblio(
                api_url, access_token, type="publication", format=format, number=number)
            description = get_patent_description(
                api_url, access_token, type="publication", format=format, number=number)
            claims = get_patent_claims(
                api_url, access_token, type="publication", format=format, number=number)

            # Add the patent to the list
            patent = {
                "number": number,
                "title": biblio.get("title"),
                "abstract": biblio.get("abstract"),
                "country": biblio.get("country"),
                "format": format,
                "type": "publication",
                "publicationDate": biblio.get("publication_date"),
                "description": description,
                "claims": claims
            }

        except Exception as e:
            # Log the error and continue with the next publication
            print(
                f"An error occurred while processing patent {number}: {e}")

    return patent


def get_patents(api_url: str, consumer_key: str, consumer_secret_key: str, query: str, first: int = 1, last: int = 10) -> list[dict]:
    """Get patents from Ops API based on the given date and type.
    Args:
        api_url (str): The Ops API URL.
        consumer_key (str): The consumer key for authentication.
        consumer_secret_key (str): The consumer secret key for authentication.
        query (str): The search query for patents in CQL language.
    Returns:
        list[dict]: A list of patents with detailed information.
    """

    # Get the access token
    access_token = get_access_token(api_url, consumer_key, consumer_secret_key)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    total_count = 2000
    first_range = first
    last_range = last
    patents = []

    while total_count > last_range:
        # Construct the URL for the patent search
        url = f"{api_url}/rest-services/published-data/search?Range={first_range}-{last_range}&q={query}"

        try:
            # Make the request to get the patents matching the criteria
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses

            # Extract the patents from the response
            patent_data = response.json()
            if not patent_data:
                raise ValueError("Patent data not found in the response.")

            # Extract the total count of patents
            total_count = int(patent_data.get("ops:world-patent-data", {}
                                              ).get("ops:biblio-search", {}).get("@total-result-count", 0))

            # Update the range for the next request
            total_count = min(total_count, 2000)
            first_range = last_range + 1
            last_range = last_range + 10
            if last_range > total_count:
                last_range = total_count

            # Extract publication references
            publications = patent_data.get("ops:world-patent-data", {}).get(
                "ops:biblio-search", {}).get("ops:search-result", {}).get("ops:publication-reference", [])

            if isinstance(publications, dict):
                publications = [publications]

            # Process each publication
            for publication in publications:
                number = None

                try:
                    document_id = publication.get("document-id", {})
                    doc_number = document_id.get(
                        "doc-number", {}).get("$", "")
                    format = document_id.get("@document-id-type", "")
                    kind = document_id.get("kind", {}).get("$", "")
                    country = document_id.get("country", {}).get("$", "")
                    number = f"{country}{doc_number}{kind}"

                    # Fetch detailed data for each patent
                    biblio = get_patent_biblio(
                        api_url, access_token, type="publication", format=format, number=number)

                    # Add the patent to the list
                    patents.append({
                        "number": number,
                        "title": biblio.get("title"),
                        "abstract": biblio.get("abstract"),
                        "country": biblio.get("country"),
                        "format": format,
                        "type": "publication",
                        "publicationDate": biblio.get("publication_date"),
                    })

                except Exception as e:
                    # Log the error and continue with the next publication
                    print(
                        f"An error occurred while processing patent {number}: {e}")

        except Exception as e:
            # Log the error and continue with the next range
            print(
                f"An error occurred while processing range {first_range}-{last_range}: {e}")

    return patents


if __name__ == "__main__":
    from pprint import pprint

    # patent = get_full_patent(
    #     api_url=ops_api_url,
    #     consumer_key=ops_consumer_key,
    #     consumer_secret_key=ops_consumer_secret_key,
    #     patent_number="EP4324636A2",
    # )
    # pprint(patent)

    patents = get_patents(
        api_url=ops_api_url,
        consumer_key=ops_consumer_key,
        consumer_secret_key=ops_consumer_secret_key,
        query="pn = EP4324636A2",
        first=1,
        last=10
    )
    for patent in patents:
        pprint(patent)
