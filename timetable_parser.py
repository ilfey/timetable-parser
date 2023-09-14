import aiohttp
import logging as log

class Parser:
    def __init__(self, base_url: str, group_id: str, login: str, password: str, session: aiohttp.ClientSession):
        self.base_url = base_url
        self._group_id = group_id
        self._login = login
        self._password = password
        self.session = session

    async def login(self):
        log.info('start login')
        async with self.session.post(f'{self.base_url}/services/security/login', json={
            'isRemember': True,
            'login': self._login,
            'password': self._password
        }) as r:
            if r.status < 300:
                log.info(f'login ended with status code: {r.status}')
            elif r.status < 500:
                log.error(f'login ended with status code: {r.status}')

    async def getTimetable(self, start, end):
        log.info('start getTimetable')
        async with self.session.get(f'{self.base_url}/services/students/{self._group_id}/lessons/{start}/{end}') as r:
            if r.status < 300:
                log.info(f'getTimetable ended with status code: {r.status}')
            elif r.status < 500:
                log.error(f'getTimetable ended with status code: {r.status}')

            res = await r.json()

            return res
