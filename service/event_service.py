from service.blockchain_service import BlockchainService


class EventService:

    def __init__(self):
        self.blockchainService = BlockchainService()
        self.web3 = self.blockchainService.get_web3()
        self.contract = self.blockchainService.get_contract()

    def get_events(self, event):
        start_block = 0
        end_block = self.web3.eth.block_number
        batch_size = 1000

        all_logs = []
        for block in range(start_block, end_block + 1, batch_size):
            batch_end_block = min(block + batch_size - 1, end_block)
            events = self.contract.events[event].get_logs(
                fromBlock=block, toBlock=batch_end_block
            )
            all_logs += [event.args for event in events]

        return all_logs

    def get_resource_created_event_by_receipt(self, txn_receipt):
        return self.contract.events.ResourceCreatedEvent().process_receipt(txn_receipt)

    def get_resource_transferred_event_by_receipt(self, txn_receipt):
        return self.contract.events.TransferSingle().process_receipt(txn_receipt)

    def get_resource_metaData_changed_event_by_receipt(self, txn_receipt):
        return self.contract.events.ResourceMetaDataChangedEvent().process_receipt(
            txn_receipt
        )
