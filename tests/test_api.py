def test_upload_csv(client, sample_csv_bytes):
    # TODO: Upload the sample CSV to POST /upload.
    # Assert status 200, six rows, two columns,
    # and a positive integer dataset ID.

    response = client.post("/upload", files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")})
    data_response = response.json()
    assert response.status_code == 200
    assert data_response["rows"] == 6
    assert data_response["columns"] == 2 
    assert data_response["id"] > 0

def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    process_response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body
    )
    assert process_response.status_code == 200
    
    process_data = process_response.json()
    assert process_data["validation_rows_removed"] == 1
    assert process_data["cleaning_report"]["rows_before"] == 5
    assert process_data["cleaning_report"]["rows_after"]

    get_response = client.get(f"/datasets/{uploaded_dataset_id}")
    assert get_response.status_code == 200
    
    get_data = get_response.json()
    assert get_data["rows"] == 3


def test_retrieve_missing_dataset(client):
    # TODO: Retrieve a dataset ID that does not exist.
    # Assert status 404.
    invalid = 349348
    response = client.get(f"/datasets/{invalid}")
    assert response.status_code == 404
