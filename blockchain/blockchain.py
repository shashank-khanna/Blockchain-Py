import hashlib
import json
import logging
from collections import namedtuple
from time import time

TRANSACTION = namedtuple("Transaction", ['From', 'To', 'Amount'])

BLOCK = namedtuple("Block", ['Index', 'Timestamp', 'Transactions', 'Hash', 'PreviousHash'])

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class BlockChain(object):

    def __init__(self):
        """
            Initialization of our basic BlockChain data structure.
            This init process also takes care of creating a genesis block.

        <chain> - This the structure that connects all our blocks
        <current> - List of new transactions that need to be added to the blockchain

        """
        self.chain = []
        self.current = []

        #  Let's create a genesis block
        self.create_block(is_genesis=True)

    def get_size(self):
        """
            Returns current length of the BlockChain

        :return: <int>
        """
        logging.debug("# Current chain size is %d" % len(self.chain))
        return len(self.chain)

    def get_last_block(self):
        """
            Returns Last Block from the BlockChain.
            Block returned is of Type <namedtuple> "Block" defined at the beginning of this file
            If BlockChain is empty, then return None

        :return: <Block>
        """
        if self.chain:
            logging.info("Chain exists and is of size %d. Returning last block" % self.get_size())
            return self.chain[-1]
        logging.warn("No Chain exists!!!")
        return None

    def create_transaction(self, sender, recipient, amount):
        """
            Consumed sender, recipient, and amount provided as arguments and generates a new Transaction
            of type <namedtuple> "Transaction" defined at the beginning of this file.
            This transaction object is then added to the list of current/pending transactions to be mined
            and is also returned.

        :param sender: <str> Name or Address of the sender
        :param recipient: <str> Name or Address of the recipient
        :param amount: <float> Amount being transferred from Sender to Recipient
        :return: <Transaction>
        """
        transaction = TRANSACTION(sender, recipient, amount)
        self.current.append(transaction)
        logging.info("Transaction successfully added. Number of Transactions now pending are %d " % len(self.current))
        return transaction

    def _reset_current_transactions(self):
        """
            Attempts to clear up current transaction queue,
            provided all of them have been added to the most recent block mined
        :return: <bool> True, if successful else False
        """
        if not self.current:
            logging.info("Current Queue has no pending transactions. Hence, nothing to reset")
            return True
        elif self.chain and self.chain[-1].Transactions == self.current:
            logging.info("Last Block in the BlockChain contains all the current/pending transactions.")
            logging.info("This means the block has been mined and we can remove these transactions from current queue")
            self.current = []
            return True
        logging.error("Some issue that needs to be investigated")
        raise IOError("Either BlockChain is invalid or we have issue with Current Transactions queue")

    def create_block(self, is_genesis=False):
        """
            Consumed Previous Hash and Proof to generate a new Proof using Proof of Work algorithm.
            This new proof is then associated with a new Block along with all the current transactions.
            This block is then inserted into the BlockChain and current transaction queue is emptied.
        :param is_genesis: Boolean flag denoting whether it needs to create a Genesis (i.e. first) block or not
        :return: <Block>
        """
        if is_genesis:
            proof = "100"
            previous_hash = "1"
            block = BLOCK(self.get_size() + 1, time(), self.current, proof, previous_hash)
        else:
            proof = self._generate_proof_of_work()
            previous_hash = self.hash_block(self.get_last_block())
            block = BLOCK(self.get_size() + 1, time(), self.current, proof, previous_hash)
        logging.info("################# Mining Started ######################")

        self.chain.append(block)
        self._reset_current_transactions()
        logging.info("### Successfully mined a new Block # %s" % block.Index)
        logging.info("### Previous Hash was: %s" % previous_hash)
        logging.info("### Current Hash generated via PoW: %s" % proof)
        logging.info("################# Mining Completed ####################")
        return block

    def _generate_proof_of_work(self):
        """
        Basic Proof of Work Algorithm that takes Last Block from the chain and then find a number "proof";
        such that when SHA256 hash of Proof and Last Proof starts with 4 zeroes.

        :return: <int> Proof value to be associated with new Block
        """

        last_block = self.get_last_block()
        last_proof = last_block.Hash
        last_hash = self.hash_block(last_block)

        proof = 0
        while self.validate_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    def _create_fee_transaction(self):
        """
            Creates an administrative transaction that can mimic a Miner Fee

        :return: <Transaction>
        """
        fee = TRANSACTION("Blockchain", "Us", 1)
        self.current.append(fee)
        logging.debug("Successfully created a Miner fee transaction")
        return fee

    def get_chain(self):
        """
            Print existing BlockChain
        :return: <list> List of Blocks
        """
        logging.debug("###### Full chain trace: Started ########")
        logging.info(self.chain)
        logging.debug("###### Full chain trace: Ended   ########")
        return self.chain

    @staticmethod
    def validate_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = str('%s%s%s' % (last_proof, proof, last_hash)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash_block(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


if __name__ == '__main__':
    blockchain = BlockChain()
    print(blockchain.get_size())
    print(blockchain.get_last_block())
    print(blockchain.create_block())
    blockchain.create_transaction("A", "B", 1)
    blockchain.create_transaction("A", "B", 2)
    blockchain.create_transaction("A", "B", 3)
    blockchain.create_transaction("A", "B", 4)
    blockchain.create_transaction("A", "B", 5)
    blockchain.create_block()
    blockchain.get_size()
    blockchain.get_chain()
    last_block = blockchain.get_last_block()
    print("Last Block received")
    print(last_block.Index)
    print(last_block.Hash)
    print(last_block)
