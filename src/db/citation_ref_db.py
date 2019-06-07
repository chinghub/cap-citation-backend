#
#
#
from datetime import datetime
import logging
from abc import ABC, abstractmethod

import boto3
from boto3.dynamodb.conditions import Key

KEY_ID_KEY = "CAPDBKEY_ID"
KEY_KEY = "CAPDBKEY"

LOGGER = logging.getLogger(__name__)


def get_citation_refs(cap_id, include_body=False):
    """
    search db for urls that have been extracted from this cap id

    optionally include the cached version of the document that is referred to
    """
    # TODO
    pass


class DynamoDB:
    __DB = None

    @classmethod
    def _get_db(cls):

        if cls.__DB:
            return cls.__DB

        session = boto3.Session(profile_name="capsvc")
        cls.__DB = session.resource("dynamodb", region_name="us-west-2")

        # cls.__DB = boto3.resource(
        #     "dynamodb", region_name="us-west-2"
        # )

        # cls.__DB = x

        # try:
        #     cls.__DB = boto3.resource(
        #         "dynamodb", region_name=Environment.getAWSRegion()
        #     )
        # except (NoCredentialsError, NoRegionError):
        #     key_id = os.getenv(cls._KEY_ID_KEY)
        #     key = os.getenv(cls._KEY_KEY)
        #
        #     cls.__DB = boto3.resource(
        #         "dynamodb",
        #         region_name=Environment.getAWSRegion(),
        #         aws_access_key_id=key_id,
        #         aws_secret_access_key=key,
        #     )

        return cls.__DB


class DynamoTable(ABC):
    @classmethod
    def _get_table(cls):
        """return the base name of the dynamodb table"""
        return DynamoDB._get_db().Table(cls.TABLENAME)

    @classmethod
    @abstractmethod
    def get_key(cls):
        pass

    @abstractmethod
    def delete(self):
        pass

    def save(self):
        return self._get_table().put_item(Item=self.data)


class CapCase(DynamoTable):
    TABLENAME = "CapCases"

    @classmethod
    def get_by_id(cls, case_id):
        resp = cls._get_table().query(
            KeyConditionExpression=Key("CapCaseId").eq(case_id)
        )
        print("get by id: {}".format(resp))
        try:
            return resp["Items"][0]
        except IndexError:
            return None

    @classmethod
    def save(cls, cap_case_id, cap_case_body):
        cls._get_table().put_item(
            Item={"CapCaseId": cap_case_id, "Document": cap_case_body}
        )


class CapCaseRef(DynamoTable):

    TABLENAME = "CapCaseRefs"

    @classmethod
    def get_latest_ref_by_id(cls, cap_case_id):
        resp = cls._get_table().query(
            KeyConditionExpression=Key("CapCaseId").eq(cap_case_id), Limit=1
        )
        return resp['Items']

    @classmethod
    def save(cls, cap_case_id, document):
        ref_time = int(datetime.utcnow().timestamp())
        LOGGER.error({'message': 'saving doc', 'cci': cap_case_id, 'ref_time': ref_time, 'document': document})
        cls._get_table().put_item(
            Item={
                'CapCaseId': cap_case_id,
                'ProcessTime': ref_time,
                'Document': document
            }
        )
