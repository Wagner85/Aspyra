from os import environ
from dataclasses import dataclass
from asyncio import gather, create_task, get_event_loop
from pandas import DataFrame
from dotenv import load_dotenv
from aiohttp import ClientSession, BasicAuth
@dataclass
class Freshservice:
    token: str
    async def get_ticket_requested_items(self, session: ClientSession, ticket_id: str) -> dict:
        """
        Get requested items in ticket form.
        Args:
            session: aiohttp session for async requests.
            ticket_id: ID of desired ticket.
        Returns:
            Dict of requested item values with ticket_id as another key.
        """
        async with session.get(f"{environ['freshservice_tickets']}/{ticket_id}/requested_items.json",
                               auth=BasicAuth(self.token, 'X')) as response:
            response_json = await response.json()
            if response_json:
                response_json = {
                    "ticket_id": ticket_id,
                    "catalog_id": response_json[0]["requested_item"]["item_display_id"],
                    "catalog_item": response_json[0]["requested_item"]["catalog_item"],
                    **response_json[0]["requested_item"]["requested_item_values"]
                }
        return response_json
    async def get_tickets_view(self, session: ClientSession, view_id: str, page_number: int = 1) -> list:
        """
        Get thirty tickets in reverse chronological order from Freshservice view.
        Args:
            view_id: ID of desired view to filter tickets.
            page_number: View pagination number.
        Returns:
            List of at most thirty tickets in JSON format.
        """
        headers = {'Content-Type': 'application/json'}
        async with session.get(f"{environ['freshservice_tickets']}/view/{view_id}?format=json&page={page_number}",
                               auth=BasicAuth(self.token, 'X'), headers=headers) as response:
            response_json = await response.json()
        return response_json
async def main():
    async with ClientSession() as session:
        fresh = Freshservice(environ["freshservice_token"])
        ticket_list = await fresh.get_tickets_view(session, environ["freshservice_view_id"])
        tickets_items = await gather(*[
            create_task(fresh.get_ticket_requested_items(session, ticket["display_id"])) for ticket in ticket_list
        ])
        print(len(tickets_items))
        DataFrame(tickets_items).to_csv("example.csv", index=False)
        # for ticket in tickets_items:
        #     if ticket["catalog_id"] == "123":
        #         response = requests.post("https://stackstorm.stone.com.br/endpoint_do_banco", headers=headers, data=data)
        #         if response.json()["status"] == "Executado com sucesso":
        #             requests.post("endpoint_do_amigo", data={"fecha o ticket do amigo"})
        #     elif ticket["catalog_id"] == "456":
        #         requests.post("https://stackstorm.stone.com.br/endpoint_da_batata", headers=headers, data=data)
        #     elif ticket["catalog_id"] == "789":
        #         requests.post("https://stackstorm.stone.com.br/endpoint_do_tomate", headers=headers, data=data)
        return "Success"
if __name__ == "__main__":
    load_dotenv()
    loop = get_event_loop()
    loop.run_until_complete(main())
