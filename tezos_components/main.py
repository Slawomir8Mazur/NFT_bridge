import smartpy as sp

class FA2(sp.Contract):
    def __init__(self, params):
        self.init(
            administrator = params.admin_address,
            all_tokens = 0,
            ledger = {},
            metadata = {'' : sp.bytes('0x68747470733a2f2f6578616d706c652e636f6d')},
            operators = {},
            paused = False,
            token_metadata = sp.big_map(
                tkey=sp.TNat, 
                tvalue=sp.TRecord(
                    token_id=sp.TNat, 
                    token_info=sp.TMap(k=sp.TString, v=sp.TBytes)
                )
            )
        )

    @sp.entry_point
    def balance_of(self, params):
        sp.verify(~ self.data.paused, 'FA2_PAUSED')
        sp.set_type(params, sp.TRecord(callback = sp.TContract(sp.TList(sp.TRecord(balance = sp.TNat, request = sp.TRecord(owner = sp.TAddress, token_id = sp.TNat).layout(("owner", "token_id"))).layout(("request", "balance")))), requests = sp.TList(sp.TRecord(owner = sp.TAddress, token_id = sp.TNat).layout(("owner", "token_id")))).layout(("requests", "callback")))
        def f_x0(_x0):
            # sp.verify(self.data.token_metadata.contains(_x0.token_id), 'FA2_TOKEN_UNDEFINED')
            sp.if self.data.ledger.contains((sp.set_type_expr(_x0.owner, sp.TAddress), sp.set_type_expr(_x0.token_id, sp.TNat))):
                sp.result(sp.record(request = sp.record(owner = sp.set_type_expr(_x0.owner, sp.TAddress), token_id = sp.set_type_expr(_x0.token_id, sp.TNat)), balance = self.data.ledger[(sp.set_type_expr(_x0.owner, sp.TAddress), sp.set_type_expr(_x0.token_id, sp.TNat))].balance))
            sp.else:
                sp.result(sp.record(request = sp.record(owner = sp.set_type_expr(_x0.owner, sp.TAddress), token_id = sp.set_type_expr(_x0.token_id, sp.TNat)), balance = 0))
        responses = sp.local("responses", params.requests.map(sp.build_lambda(f_x0)))
        sp.transfer(responses.value, sp.tez(0), sp.set_type_expr(params.callback, sp.TContract(sp.TList(sp.TRecord(balance = sp.TNat, request = sp.TRecord(owner = sp.TAddress, token_id = sp.TNat).layout(("owner", "token_id"))).layout(("request", "balance"))))))

    @sp.entry_point
    def mint(self, params):
        sp.verify(sp.sender == self.data.administrator, 'FA2_NOT_ADMIN')
        sp.if self.data.ledger.contains((sp.set_type_expr(params.address, sp.TAddress), sp.set_type_expr(params.token_id, sp.TNat))):
            self.data.ledger[(sp.set_type_expr(params.address, sp.TAddress), sp.set_type_expr(params.token_id, sp.TNat))].balance += params.amount
        sp.else:
            self.data.ledger[(sp.set_type_expr(params.address, sp.TAddress), sp.set_type_expr(params.token_id, sp.TNat))] = sp.record(balance = params.amount)
        self.data.all_tokens += 1
        self.data.token_metadata[params.token_id] = sp.record(token_id = params.token_id, token_info = params.metadata)

    @sp.entry_point
    def set_administrator(self, params):
        sp.verify(sp.sender == self.data.administrator, 'FA2_NOT_ADMIN')
        self.data.administrator = params

    @sp.entry_point
    def set_metadata(self, params):
        sp.verify(sp.sender == self.data.administrator, 'FA2_NOT_ADMIN')
        self.data.metadata[params.k] = params.v

    @sp.entry_point
    def set_pause(self, params):
        sp.verify(sp.sender == self.data.administrator, 'FA2_NOT_ADMIN')
        self.data.paused = params

    @sp.entry_point
    def transfer(self, params):
        sp.verify(~ self.data.paused, 'FA2_PAUSED')
        sp.set_type(params, sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))))
        sp.for transfer in params:
            sp.for tx in transfer.txs:
                sp.verify(((sp.sender == self.data.administrator) | (transfer.from_ == sp.sender)) | (self.data.operators.contains(sp.set_type_expr(sp.record(owner = transfer.from_, operator = sp.sender, token_id = tx.token_id), sp.TRecord(operator = sp.TAddress, owner = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id")))))), 'FA2_NOT_OPERATOR')
                # sp.verify(self.data.token_metadata.contains(tx.token_id), 'FA2_TOKEN_UNDEFINED')
                sp.if tx.amount > 0:
                    sp.verify(self.data.ledger[(sp.set_type_expr(transfer.from_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))].balance >= tx.amount, 'FA2_INSUFFICIENT_BALANCE')
                    self.data.ledger[(sp.set_type_expr(transfer.from_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))].balance = sp.as_nat(self.data.ledger[(sp.set_type_expr(transfer.from_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))].balance - tx.amount)
                    sp.if self.data.ledger.contains((sp.set_type_expr(tx.to_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))):
                        self.data.ledger[(sp.set_type_expr(tx.to_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))].balance += tx.amount
                    sp.else:
                        self.data.ledger[(sp.set_type_expr(tx.to_, sp.TAddress), sp.set_type_expr(tx.token_id, sp.TNat))] = sp.record(balance = tx.amount)

    # @sp.entry_point
    # def update_operators(self, params):
    #     sp.set_type(params, sp.TList(sp.TVariant(add_operator = sp.TRecord(operator = sp.TAddress, owner = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id"))), remove_operator = sp.TRecord(operator = sp.TAddress, owner = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id")))).layout(("add_operator", "remove_operator"))))
    #     sp.for update in params:
    #         with update.match_cases() as arg:
    #             with arg.match('add_operator') as add_operator:
    #                 sp.verify((add_operator.owner == sp.sender) | (sp.sender == self.data.administrator), 'FA2_NOT_ADMIN_OR_OPERATOR')
    #                 self.data.operators[sp.set_type_expr(sp.record(owner = add_operator.owner, operator = add_operator.operator, token_id = add_operator.token_id), sp.TRecord(operator = sp.TAddress, owner = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id"))))] = sp.unit
    #             with arg.match('remove_operator') as remove_operator:
    #                 sp.verify((remove_operator.owner == sp.sender) | (sp.sender == self.data.administrator), 'FA2_NOT_ADMIN_OR_OPERATOR')
    #                 del self.data.operators[sp.set_type_expr(sp.record(owner = remove_operator.owner, operator = remove_operator.operator, token_id = remove_operator.token_id), sp.TRecord(operator = sp.TAddress, owner = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id"))))]


class MultiSigMintery(sp.Contract):
    def __init__(self, params):
        self.init(
            required_signatures = params.required_signatures,
            pks = params.pks,
            contracts=sp.big_map(tkey=sp.TString, tvalue=sp.TAddress)
        )

    @sp.entry_point
    def mint_token(self, params):
        self.verify_signatures(params.signatures_paramteres)
        contract = sp.contract(
            sp.TRecord(address=sp.TAddress, token_id=sp.TNat, 
                       amount=sp.TNat, metadata=sp.TMap(k=sp.TString, v=sp.TBytes)), 
            self.data.contracts[params.source_contract], 
            "mint"
        ).open_some()
        sp.transfer(params.mint_params, sp.tez(0), contract)

    @sp.entry_point
    def burn_token(self, params):
        self.verify_signatures(params.signatures_paramteres)

    @sp.entry_point
    def add_contract(self, params):
        self.verify_signatures(params.signatures_paramteres)
        self.data.contracts[params.eth_token_address] = params.tez_token_address

    def verify_signatures(self, params):
        counter = sp.local('counter', 0)
        sp.for sign in params.signatures:
            sp.for pk in self.data.pks:
                sp.if sp.check_signature(pk, sign, params.payload):
                    counter.value += 1
        sp.verify(counter.value >= self.data.required_signatures, "Too few valid signatures provided") 

# Tests
@sp.add_test(name = "MultiSig")
def test():

    alice    = sp.test_account("Alice")
    bob      = sp.test_account("Rob")
    charlie  = sp.test_account("Charlie")
    david    = sp.test_account("David")
    ed       = sp.test_account("Ed")

    scenario = sp.test_scenario()

    scenario.h1("Bridge")
    m = MultiSigMintery(sp.record(
        required_signatures=sp.nat(2), 
        pks=[
            alice.public_key,
            bob.public_key,
            charlie.public_key,
            david.public_key,
            ed.public_key
        ]
    ))
    scenario += m

    scenario.h1("FA2")
    c1 = FA2(sp.record(admin_address=m.address))
    scenario += c1

    scenario.h2("test add")
    message = sp.record(eth_token_address="0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c", token_id=sp.nat(10), target_owner=alice.public_key_hash)
    message_packed = sp.pack(message)
    # Passing test
    m.add_contract(sp.record(
        signatures_paramteres = sp.record(
            signatures=[
                sp.make_signature(alice.secret_key, message_packed, message_format = 'Raw'),
                sp.make_signature(charlie.secret_key, message_packed, message_format = 'Raw')
            ],
            payload=message_packed
        ),
        eth_token_address="0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c",
        tez_token_address=c1.address))
    # Failing test
    m.add_contract(sp.record(
        signatures_paramteres = sp.record(
            signatures=[
                sp.make_signature(charlie.secret_key, message_packed, message_format = 'Raw')
            ],
            payload=message_packed
        ),
        eth_token_address="0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c",
        tez_token_address=alice.address)).run(valid=False)

    # das
    m.mint_token(sp.record(
        signatures_paramteres = sp.record(
            signatures=[
                sp.make_signature(alice.secret_key, message_packed, message_format = 'Raw'),
                sp.make_signature(charlie.secret_key, message_packed, message_format = 'Raw')
            ],
            payload=message_packed
        ),
        source_contract="0xD0a7efE60Fd0850FDc2A63795a4a55460e732f1c",
        mint_params = sp.record(
            amount=sp.nat(1),
            address=alice.address,
            token_id=sp.nat(10),
            metadata={"": sp.bytes("0x1234")}
        )
        ))