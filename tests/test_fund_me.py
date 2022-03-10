from brownie import FundMe, network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest

def test_can_fund_and_withdraw():
    #arrange
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    #act fund
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    #assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    #act withdraw
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    #assert
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS: #NOT DEV network
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_address = accounts.add() #random account

    #act
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_address})
