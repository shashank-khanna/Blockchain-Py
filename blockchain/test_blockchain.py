from unittest import TestCase

from blockchain.blockchain import BlockChain


class TestBlockChain(TestCase):

    def setUp(self):
        self.block_chain = BlockChain()

    def test_get_size(self):
        self.assertEquals(len(self.block_chain.chain), self.block_chain.get_size(), "# Chain Size does not match!!")

    def test_get_last_block(self):
        last_block = self.block_chain.get_last_block()
        self.assertIsNotNone(last_block.Hash)
        self.assertIsNotNone(last_block.Index)
        self.assertIsNotNone(last_block.PreviousHash)
        self.assertIsNotNone(last_block.Transactions)
        self.assertIsNotNone(last_block.Timestamp)

    def test_create_transaction(self):
        transaction = self.block_chain.create_transaction("A", "B", 100)
        self.assertEqual(transaction.From, "A", "Sender and From in Transaction created not matching ")
        self.assertEqual(transaction.To, "B", "Recipient and To in Transaction created not matching ")
        self.assertEqual(transaction.Amount, 100, "Amount and Amount in Transaction not matching")

    def test_create_block(self):
        block = self.block_chain.create_block(is_genesis=False)
        self.assertEqual(block.Index, len(self.block_chain.chain))
        self.assertIsNotNone(block.Hash)
        self.assertIsNotNone(block.PreviousHash)
        self.assertIsNotNone(block.Transactions)
        self.assertIsNotNone(block.Timestamp)
        self.assertEqual(block, self.block_chain.get_last_block())
        self.assertEqual(self.block_chain.current, [])

    def test_get_chain(self):
        chain = self.block_chain.get_chain()
        self.assertEqual(chain, self.block_chain.chain)

    def test_validate_proof(self):
        block1 = self.block_chain.create_block(is_genesis=False)
        block2 = self.block_chain.create_block(is_genesis=False)
        self.assertTrue(BlockChain.validate_proof(last_proof=block1.Hash, proof=block2.Hash,
                                                  last_hash=BlockChain.hash_block(block1)),
                        "Proof of Work Hash in the last block does not align with Second Last block. Chain Corrupt!!!")


if __name__ == '__main__':
    import unittest

    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlockChain)
    unittest.TextTestRunner(verbosity=2).run(suite)
