import asyncio

from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from crawlee.storages import RequestQueue, Dataset
from crawlee.fingerprint_suite import (
    DefaultFingerprintGenerator,
    HeaderGeneratorOptions,
    ScreenOptions
)
from crawlee.sessions import SessionCookies, SessionPool
from datetime import timedelta, datetime

async def main() -> None:
    
    dataset = await Dataset.open()
    rq = await RequestQueue.open()
    
    crawler = BeautifulSoupCrawler(
        # request_manager=rq,
        max_request_retries=3,
        max_requests_per_crawl=10,
        use_session_pool=True,
        session_pool=SessionPool(
            max_pool_size=1,
            create_session_settings={
                'max_usage_count': 999_999,
                'max_age': timedelta(999_999),
                'max_error_score': 100,
                'blocked_status_codes': [403]
            }
        )
    )
    
    page = 1
    url = f"https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=AD08DE2179&page={page}&order=DateDesc"
    
    await rq.add_request(url)
    
    # Basic request handling logic
    @crawler.router.default_handler
    async def request_handler(
        context: BeautifulSoupCrawlingContext 
    ) -> None:
        
        url = context.request.url,
        context.log.info(f"Processing '{url}'")
        
        # Enqueue links found within elements that match the specified selector.
        # These links will be added to the crawling queue with the label RENT_OBJECTS.
        await context.enqueue_links(
            selector='.css-xt08q3',
            label='RENT_OBJECTS'
        )
        
        if context.request.label == 'RENT_OBJECTS':
        
            expose_id = url[0].split('/')[4], # assumes https://www.immowelt.de/expose/<expose-id>
            title = context.soup.title.string if context.soup.title else None

            rent_type = context.soup.select_one(
                "div.css-8g8ihq > span.css-2bd70b")
            cold_rent = context.soup.select_one(
                "div.css-8g8ihq > div > span.css-1gs73yw")
            number_of_rooms = context.soup.select_one(
                "div.css-9sumw7 > div:nth-child(1) > div > div > span.css-2bd70b")
            living_space_m2 = context.soup.select_one(
                "div.css-9sumw7 > div:nth-child(2) > div > div > span.css-2bd70b")
            floor = context.soup.select_one(
                "div.css-9sumw7 > div:nth-child(3) > div > div > span.css-2bd70b")
            equipment_features = context.soup.select(
                "div.css-1goi9xp > main > div.css-18xl464.MainColumn > div > section:nth-child(5) > div.css-1j9uv53 > ul > li")
            location = context.soup.select_one(
                "div.css-1ytyjyb")
            
            data = {
                'url': url[0],
                'title': title,
                'expose-id': expose_id,
                'rent_type': rent_type.text if rent_type is not None else "keine Angabe",
                'cold_rent': cold_rent.text if cold_rent is not None else "keine Angabe",
                'number_of_rooms': number_of_rooms.text if number_of_rooms is not None else "keine Angabe",
                'living_space_m2': living_space_m2.text if living_space_m2 is not None else "keine Angabe",
                'floor': floor.text if floor is not None else "keine Angabe",
                'equipment_features': [i.text for i in equipment_features],
                'location': location.text if location is not None else "keine Angabe",
                'loadtime': datetime.now()
            }
            context.log.info(data)
            await dataset.push_data(data)
        
    # Handler for session initialization (authentication, initial cookies, etc.)
    @crawler.router.handler(label='session_init')
    async def session_init(context: BeautifulSoupCrawlingContext) -> None:
        if context.session:
            context.log.info(f"Init session: {context.session.id}")
            
    # Monitor if our session gets blocked and explicitly stop the crawler in that case
    @crawler.error_handler
    async def error_handling(context: BeautifulSoupCrawlingContext) -> None:
        if isinstance(error, SessionError):
            context.log.info(
                f'Session {context.session.id} blocked. Stopping crawler')
            crawler.stop()
        
    await crawler.run()
    await crawler.export_data_json(path="results.json")
    
if __name__ == '__main__':
    asyncio.run(main())