import requests

BORROWERS_PATH = "src/borrowers.sol"

AAVE_GRAPH_URLS = {
    "ethereum_v2": "https://api.thegraph.com/subgraphs/name/aave/protocol-v2",
    "polygon_v3": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-polygon",
    "avalanche_v3": "https://api.thegraph.com/subgraphs/name/yonach/aave-v3-avalanche",
    "arbitrum_v3": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-arbitrum",
    "optimism_v3": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-optimism-fix",
    "fantom_v3": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-fantom",
    "harmony_v3": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-harmony",
    "ethereum_v3": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3",
}

print("start fetching borrowers")

addresses = []
# aave_top_accounts = f"""
#       {{
#           userReserves(first: 1000, orderBy: currentTotalDebt, orderDirection: desc, where: {{id_gt: "{last_id}"}}) {{
#             id
#             user {{
#               id
#             }}
#           }}
#         }}
#       """

aave_top_account_per_reserve = """  {pools{
    reserves{
      symbol
      userReserves(first:10, orderBy: currentATokenBalance, orderDirection: desc){
        user{
          id
        }
      }
    }
  }
  }
     """

response = requests.post(
    AAVE_GRAPH_URLS["ethereum_v3"], json={"query": aave_top_account_per_reserve}, )
data = response.json()['data']['pools'][0]['reserves']
print("finished fetching borrowers")
print(data)
for reserve_data in data:
    for account_data in reserve_data['userReserves']:
        addresses.append(account_data['user']['id'])


print("before remove duplicates: ", len(addresses))
addresses = list(dict.fromkeys(addresses))
print("after remove duplicates: ", len(addresses))

addresses_code = ""
for address in addresses:
    pad_address = "address(" + address[0:2] + \
        "00" + address[2:len(address)] + "),"
    addresses_code += pad_address


with open(BORROWERS_PATH, 'w') as f:
    template = f"""
    // SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract Constants {{
  address[] public arr;

  function getBorrowers() public returns (address[] memory) {{
    arr = [
{addresses_code[0:-1]}
    ];
    return arr;
  }}
}}

    """
    f.write(template)
print(f"update borrowers in: {BORROWERS_PATH}")