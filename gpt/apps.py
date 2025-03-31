from django.apps import AppConfig
from CryptoryDjango import settings
import requests
import logging

class GptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gpt'

class EurekaConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # ECS Public IP 조회
        aws_metadata_template = AwsMetadataTemplate()
        token = aws_metadata_template.create_token()
        if token:
            public_ip = aws_metadata_template.get_public_ip(token)
            if public_ip:
                self.register_service_with_eureka(public_ip)

    def register_service_with_eureka(self, public_ip):
        """Eureka에 서비스 등록"""
        eureka_url = settings.EUREKA_URL  # 예: 'http://localhost:8761/eureka/apps/'
        service_name = settings.SERVICE_NAME  # 예: 'MY-SERVICE'
        service_host = public_ip  # ECS의 public IP
        service_port = 8000  # 서비스 포트
        instance_id = f"{service_name}:{service_host}:{service_port}"

        payload = {
            'instance': {
                'instanceId': instance_id,
                'hostName': service_host,
                'app': service_name,
                'ipAddr': service_host,
                'port': {'$': service_port, '@enabled': 'true'},
                'statusPageUrl': f'http://{service_host}:{service_port}/actuator/health',
                'healthCheckUrl': f'http://{service_host}:{service_port}/actuator/health',
                'vipAddress': service_name,
                'secureVipAddress': service_name
            }
        }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(f"{eureka_url}/{service_name}/", json=payload, headers=headers)
            if response.status_code == 204:
                print(f"Service {service_name} registered with Eureka successfully!")
            else:
                print(f"Failed to register service {service_name} with Eureka: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error registering service with Eureka: {e}")
            

class AwsMetadataTemplate:
    META_URL = "http://169.254.170.2/v3/metadata"
    TOKEN_TTL_HEADER = "X-aws-ec2-metadata-token-ttl-seconds"
    TOKEN_HEADER = "X-aws-ec2-metadata-token"
    TOKEN_TTL = "3600"  # 60분
    VERSION = "latest"

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create_token(self):
        """ECS Metadata Token 생성"""
        headers = {self.TOKEN_TTL_HEADER: self.TOKEN_TTL}
        try:
            response = requests.put(f"{self.META_URL}/api/token", headers=headers, timeout=2)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.log.warning("AWS 메타데이터 토큰을 생성하는데 실패했습니다: %s", e)
            return None

    def get_public_ip(self, token):
        """ECS Public IP 조회"""
        headers = {self.TOKEN_HEADER: token}
        try:
            response = requests.get(f"{self.META_URL}/task|jq -r '.Containers[0].Networks[0].IPv4Addresses[0]'", headers=headers, timeout=2)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            self.log.warning("AWS 메타데이터에서 Public IP를 가져오는 데 실패했습니다: %s", e)
            return None