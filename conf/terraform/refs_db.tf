resource "aws_dynamodb_table" "cap_citation_refs_dynamo_table" {
  name = "CapCitationRefs"
  read_capacity = 1
  write_capacity = 1
  hash_key = "CapId"

  attribute {
    name = "CapId"
    type = "S"
  }

  tags {
    Name = "CapCitationRefs"
    Environment = "DEV"
  }
}
