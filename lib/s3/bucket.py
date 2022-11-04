class S3_Bucket:
    def __init__(
        self, s3_resource, s3_client, bucket_name: str, region: str = None
    ) -> None:
        self.resource = s3_resource
        self.client = s3_client
        self.bucket_name = bucket_name
        self.bucket = s3_resource.Bucket(bucket_name)
        if not self.exists:
            if not region:
                raise f"Bucket {self.bucket_name} is missing -  specify region"
            print(f"Bucket {self.bucket_name} is missing - creating now")
            self.create_bucket(region=region)

    def upload_file(self, file_name: str, data: bytes):
        object = self.resource.Object(self.bucket_name, file_name)
        result = object.put(Body=data)
        return result["ResponseMetadata"]["HTTPStatusCode"] == 200

    def create_bucket(self, region: str):
        location = {"LocationConstraint": region}
        self.client.create_bucket(
            Bucket=self.bucket_name, CreateBucketConfiguration=location
        )

    def download_file(self, s3_path: str):
        return self.client.get_object(Bucket=self.bucket_name, Key=s3_path)[
            "Body"
        ].read()

    @property
    def exists(self) -> bool:
        buckets = self.client.list_buckets()["Buckets"]
        _ = [item for item in buckets if item["Name"] == self.bucket_name]
        return len(_) == 1
