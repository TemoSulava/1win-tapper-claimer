import string
import aiohttp
import asyncio
import random
import base64
import os

from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
from utils.core import logger
from data import config


class OneWin:
    REQUIRED = config.REQUIRED
    PRICES = config.PRICES
    TOOLS = config.TOOLS

    def __init__(self, thread: int, account: str, proxy: str):
        self.thread = thread
        self.name = account
        self.proxy = self._configure_proxy(proxy)
        self.client = self._create_client(account, proxy)
        self.session = self._create_session()
        self.balance = 0

    def _configure_proxy(self, proxy):
        if proxy:
            proxy_parts = proxy.split(':')
            return f"{config.PROXY_TYPE}://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"
        return None

    def _create_client(self, account, proxy):
        proxy_client = None
        if proxy:
            proxy_parts = proxy.split(':')
            proxy_client = {
                "scheme": config.PROXY_TYPE,
                "hostname": proxy_parts[0],
                "port": int(proxy_parts[1]),
                "username": proxy_parts[2],
                "password": proxy_parts[3],
            }
        return Client(
            name=account,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy_client,
        )

    def _create_session(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,bg;q=0.6,mk;q=0.5',
            'cache-control': 'no-cache',
            'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent(os='android').random,
        }
        return aiohttp.ClientSession(
            headers=headers, trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)
        )

    async def main(self):
        if not await self.login():
            await self.session.close()
            return 0

        logger.info(
            f"main | Thread {self.thread} | {self.name} | Start! | PROXY : {self.proxy}")
        while True:
            try:
                info = await self.mining_info()
                if info is None:
                    logger.error(
                        f"main | Thread {self.thread} | {self.name} | mining_info returned None")
                    await asyncio.sleep(random.uniform(30, 60))
                    continue
                logger.info(
                    f"main | Thread {self.thread} | {self.name} | Mining info: {info}")
                await self._process_tools(info)
                await self.everydayreward()
                for _ in range(random.randint(1, 100)):
                    await self.tap()
            except Exception as err:
                logger.error(
                    f"main | Thread {self.thread} | {self.name} | {err}")
                await asyncio.sleep(random.uniform(30, 60))

    async def _process_tools(self, info):
        for tool in reversed(list(self.REQUIRED.keys())):
            if tool not in info:
                tool, price = self._check_tool_requirements(tool, info)
                if price and self.balance >= price:
                    await self.upgrade(tool)
            else:
                if info[tool] < config.UPGRADE_LEVEL:
                    tool, price = self._get_tool_upgrade(tool, info)
                    if price and self.balance >= price:
                        await self.upgrade(tool)

    def _check_tool_requirements(self, tool, info):
        if self.REQUIRED[tool] is None:
            tool += '1'
            price = self.PRICES.get(tool)
        else:
            required = self.REQUIRED[tool].translate(
                str.maketrans('', '', string.digits))
            if required in info and info[required] >= int(self.REQUIRED[tool].replace(required, '')):
                tool += '1'
                price = self.PRICES.get(tool)
            else:
                price = None
        return tool, price

    def _get_tool_upgrade(self, tool, info):
        tool += str(info[tool] + 1)
        price = self.PRICES.get(tool)
        return tool, price

    async def upgrade(self, name):
        await self.get_balance()
        self.session.headers['content-type'] = 'application/json'
        json_data = {'id': name}
        logger.info(
            f"upgrade | Thread {self.thread} | {self.name} | Upgrading tool: {name}")
        response = await self.session.post('https://crypto-clicker-backend-go-prod.100hp.app/minings', json=json_data, proxy=self.proxy)

        await self._handle_response(response, 'upgrade')
        await self._reset_headers()
        await asyncio.sleep(random.uniform(4, 8))
        await self.get_balance()

    async def _handle_response(self, response, context):
        content_type = response.headers.get('Content-Type')
        if response.status == 200 and response.content_length == 0:
            logger.warning(
                f"{context} | Thread {self.thread} | {self.name} | Empty response received")
        elif content_type and 'application/json' in content_type:
            answer = await response.json()
            tool = answer.get('NextLevel').get('id').translate(
                str.maketrans('', '', string.digits))
            logger.success(
                f"{context} | Thread {self.thread} | {self.name} | Upgrade {tool} to {answer.get('NextLevel').get('level') - 1} LEVEL")
        else:
            response_text = await response.text()
            logger.warning(
                f"{context} | Thread {self.thread} | {self.name} | Unexpected response type: {content_type}, Response text: {response_text}")

    async def _reset_headers(self):
        del self.session.headers['content-type']
        authorization = self.session.headers['authorization']
        del self.session.headers['authorization']
        self.session.headers['access-control-request-headers'] = 'authorization,content-type'
        self.session.headers['access-control-request-method'] = 'POST'
        await self.session.options('https://crypto-clicker-backend-go-prod.100hp.app/minings', proxy=self.proxy)
        del self.session.headers['access-control-request-headers']
        del self.session.headers['access-control-request-method']
        self.session.headers['authorization'] = authorization

    async def mining_info(self):
        try:
            response = await self.session.get('https://crypto-clicker-backend-go-prod.100hp.app/minings', proxy=self.proxy)
            await self._reset_options_headers('GET', 'https://crypto-clicker-backend-go-prod.100hp.app/minings')
            response = await response.json()
            if response is None:
                logger.error("mining_info | Response is None")
                return None

            return {tool['id'].translate(str.maketrans('', '', string.digits)): tool['level'] for tool in response}
        except Exception as err:
            logger.error(f"mining_info | {err}")
            return None

    async def everydayreward(self):
        try:
            response = await self.session.get("https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward", proxy=self.proxy)
            resp = await response.json()
            day_data = resp.get('days')[0]
            logger.info(
                f"everydayreward | Thread {self.thread} | {self.name} | Day: {day_data['id']}, Reward: {day_data['money']}, Is Collected: {day_data['isCollected']}")

            if not day_data['isCollected']:
                await self.session.post('https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward', proxy=self.proxy)
                await self._reset_options_headers('POST', 'https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward')
                logger.success(
                    f"everyday | Thread {self.thread} | {self.name} | claim {day_data['id']} reward : {day_data['money']}")

            await self.get_balance()
        except Exception as err:
            logger.error(f"everydayreward | {err}")

    async def tap(self):
        self.session.headers['content-type'] = 'application/json'
        taps_count = random.randint(*config.TAPS_COUNT_RANGE)
        json_data = {'tapsCount': taps_count}
        logger.info(
            f"tap | Thread {self.thread} | {self.name} | Tapping with count: {json_data['tapsCount']}")
        try:
            response = await self.session.post('https://crypto-clicker-backend-go-prod.100hp.app/tap', json=json_data, proxy=self.proxy)
            await self._handle_response(response, 'tap')
        except Exception as err:
            logger.error(
                f"tap | Thread {self.thread} | {self.name} | Error during tap request: {err}")
        await self.get_balance()
        await self._reset_headers()

    async def _reset_options_headers(self, method, url):
        authorization = self.session.headers['authorization']
        del self.session.headers['authorization']
        self.session.headers['access-control-request-headers'] = 'authorization'
        self.session.headers['access-control-request-method'] = method
        await self.session.options(url, proxy=self.proxy)
        del self.session.headers['access-control-request-headers']
        del self.session.headers['access-control-request-method']
        self.session.headers['authorization'] = authorization

    async def get_balance(self):
        try:
            response = await self.session.get('https://crypto-clicker-backend-go-prod.100hp.app/user/balance', proxy=self.proxy)
            await self._reset_options_headers('GET', 'https://crypto-clicker-backend-go-prod.100hp.app/user/balance')
            answer = await response.json()
            self.balance = answer.get('coinsBalance')
            logger.info(
                f"get_balance | Thread {self.thread} | {self.name} | Balance: {self.balance}")
            await asyncio.sleep(random.uniform(1, 3))
        except Exception as err:
            logger.error(f"get_balance | {err}")

    async def login(self):
        try:
            self.session.headers[
                'content-type'] = f'multipart/form-data; boundary={self.generate_boundary()}'
            tg_web_data = await self.get_tg_web_data()
            files = {'referrer_tg_id': (None, '707649803')}
            logger.info(
                f"login | Thread {self.thread} | {self.name} | Sending login request")
            resp = await self.session.post('https://crypto-clicker-backend-go-prod.100hp.app/game/start', params=tg_web_data, data=files, proxy=self.proxy)
            del self.session.headers['content-type']
            self.session.headers['accept'] = '*/*'
            resp = await resp.json()
            self.session.headers['authorization'] = "Bearer " + \
                resp.get("token")
            await self.get_balance()
            await asyncio.sleep(random.uniform(3, 5))
            logger.success(
                f"login | Thread {self.thread} | {self.name} | Login successful")
            return True
        except Exception as err:
            logger.error(f"login | Thread {self.thread} | {self.name} | {err}")
            return False

    async def get_tg_web_data(self):
        await self.client.connect()
        try:
            bot = await self.client.resolve_peer('token1win_bot')
            app = InputBotAppShortName(bot_id=bot, short_name="start")
            web_view = await self.client.invoke(RequestAppWebView(peer=bot, app=app, platform='android', write_allowed=True, start_param="refId707649803"))
            auth_url = web_view.url
            params = self._parse_auth_url(auth_url)
        except Exception as err:
            logger.error(
                f"get_tg_web_data | Thread {self.thread} | {self.name} | {err}")
            if 'USER_DEACTIVATED_BAN' in str(err):
                logger.error(
                    f"login | Thread {self.thread} | {self.name} | USER BANNED")
                await self.client.disconnect()
                return False
        await self.client.disconnect()
        return params

    def _parse_auth_url(self, auth_url):
        parsed_url = urlparse(auth_url)
        fragment_params = parse_qs(parsed_url.fragment)
        params = {key: value[0] for key, value in fragment_params.items()}
        tg_web_app_data = parse_qs(params['tgWebAppData'])
        params.update({key: value[0]
                      for key, value in tg_web_app_data.items()})
        del params['tgWebAppData']
        del params['tgWebAppVersion']
        del params['tgWebAppPlatform']
        del params['tgWebAppSideMenuUnavail']
        return params

    def generate_boundary(self):
        return '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    def decode_param(self, encoded_param):
        decoded_bytes = base64.urlsafe_b64decode(encoded_param.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
