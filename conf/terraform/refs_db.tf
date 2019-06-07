resource "aws_dynamodb_table" "cap_cases_dynamo_table" {
  name = "CapCases"
  hash_key = "CapCaseId"

  attribute {
    name = "CapCaseId"
    type = "S"
  }

  read_capacity = 1
  write_capacity = 1

  tags = {
    Name = "CapCases"
    Environment = "DEV"
  }
}

resource "aws_dynamodb_table" "cap_case_refs_dynamo_table" {
  name = "CapCaseRefs"
  hash_key = "CapCaseId"
  range_key = "ProcessTime"

  attribute {
    name = "CapCaseId"
    type = "S"
  }

  attribute {
    name = "ProcessTime"
    type = "N"
  }

  read_capacity = 1
  write_capacity = 1

  tags = {
    Name = "CapCitationRefs"
    Environment = "DEV"
  }
}
