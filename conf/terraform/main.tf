#
# CAP Citation Terraform file
#

provider "aws" {
  region = "us-west-2"
  profile = "cap-citation-terraform"
}

terraform {
  backend "s3" {
    region = "us-west-2"
    profile = "cap-citation-terraform"
    bucket = "cap-citation-terraform-state"
    key = "CapCitationBackend/terraform.tfstate"
  }
}
