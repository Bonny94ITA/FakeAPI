from abc import ABC, abstractmethod

class ReportPipeline(ABC):
    async def run(self):
        try:
            await self.prepare()
            data = await self.fetch_data()
            cleaned = self.clean_data(data)
            aggregated = self.aggregate_data(cleaned)
            self.save_reports(aggregated)
        except Exception as e:
            self.handle_exception(e)

    async def prepare(self):
        pass  # Optional step, can be overridden

    @abstractmethod
    async def fetch_data(self):
        pass

    @abstractmethod
    def clean_data(self, data):
        pass

    @abstractmethod
    def aggregate_data(self, cleaned):
        pass

    @abstractmethod
    def save_reports(self, aggregated):
        pass

    def handle_exception(self, e):
        raise e