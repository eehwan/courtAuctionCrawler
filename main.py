#!/usr/bin/env python3
import json
import requests

COURT_CODES = {
    "서울중앙지방법원": "B000210",
    "서울동부지방법원": "B000211",
    "서울서부지방법원": "B000215",
    "서울남부지방법원": "B000212",
    "서울북부지방법원": "B000213",
    "의정부지방법원": "B000214",
    "고양지원": "B214807",
    "남양주지원": "B214804",
    "인천지방법원": "B000240",
    "부천지원": "B000241",
    "수원지방법원": "B000250",
    "성남지원": "B000251",
    "여주지원": "B000252",
    "평택지원": "B000253",
    "안산지원": "B250826",
    "안양지원": "B000254",
    "춘천지방법원": "B000260",
    "강릉지원": "B000261",
    "원주지원": "B000262",
    "속초지원": "B000263",
    "영월지원": "B000264",
    "청주지방법원": "B000270",
    "충주지원": "B000271",
    "제천지원": "B000272",
    "영동지원": "B000273",
    "대전지방법원": "B000280",
    "홍성지원": "B000281",
    "논산지원": "B000282",
    "천안지원": "B000283",
    "공주지원": "B000284",
    "서산지원": "B000285",
    "대구지방법원": "B000310",
    "안동지원": "B000311",
    "경주지원": "B000312",
    "김천지원": "B000313",
    "상주지원": "B000314",
    "의성지원": "B000315",
    "영덕지원": "B000316",
    "포항지원": "B000317",
    "대구서부지원": "B000320",
    "부산지방법원": "B000410",
    "부산동부지원": "B000412",
    "부산서부지원": "B000414",
    "울산지방법원": "B000411",
    "창원지방법원": "B000420",
    "마산지원": "B000431",
    "진주지원": "B000421",
    "통영지원": "B000422",
    "밀양지원": "B000423",
    "거창지원": "B000424",
    "광주지방법원": "B000510",
    "목포지원": "B000511",
    "장흥지원": "B000512",
    "순천지원": "B000513",
    "해남지원": "B000514",
    "전주지방법원": "B000520",
    "군산지원": "B000521",
    "정읍지원": "B000522",
    "남원지원": "B000523",
    "제주지방법원": "B000530"
}
URL_LIST = {
    "사건내역" : "https://www.courtauction.go.kr/pgj/pgj15A/selectAuctnCsSrchRslt.on",
    "기일내역" : "https://www.courtauction.go.kr/pgj/pgj15A/selectCsDtlDxdyDts.on",
    "문건/송달내역" : "https://www.courtauction.go.kr/pgj/pgj15A/selectDlvrOfdocDtsDtl.on",
}
PAYLOAD_LIST = {
    "사건내역" : "dma_srchCsDtlInf",
    "기일내역" : "dma_srchDxdyDtsLst",
    "문건/송달내역" : "dma_srchDlvrOfdocDts",
}


def main(court, csNo, tab):
    csNo1, csNo2 = csNo.split("타경")
    csNo2 = csNo2.zfill(6)

    # 브라우저처럼 보이기 위한 헤더 설정
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

    # 세션 생성 (쿠키 자동 관리)
    initial_url = "https://www.courtauction.go.kr/pgj/index.on"
    session = requests.Session()
    response = session.get(initial_url, headers=headers)
    # print(f"Initial GET status: {response.status_code}".center(50, "-"))

    headers.update({"Referer": initial_url})
    # 1. 초기 페이지 방문 - 쿠키 획득

    # 2. POST 요청 시
    post_url = URL_LIST[tab]
    payload = {
        PAYLOAD_LIST[tab]: {
            "cortOfcCd": COURT_CODES[court],
            "csNo": f"{csNo1}0130{csNo2}",
        },
    }
    if (tab == "문건/송달내역"):
        payload[PAYLOAD_LIST[tab]].update({"srchFlag":"F"})
    # print(post_url, payload)

    response = session.post(post_url, json=payload, headers=headers)
    # print("POST response:".center(50, "-"))
    try:
        data = response.json().get("data")
        return data
    except Exception as err:
        print("JSON 파싱 중 오류 발생:", err)
        print("응답 내용:", response.text)
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="법원 경매 정보 요청 스크립트",
    )
    # 선택적 positional argument: 법원명 (기본값: 서울중앙지방법원)
    parser.add_argument(
        "court",
        nargs="?",
        default="서울중앙지방법원",
        choices=COURT_CODES.keys(),
        metavar="court",
        help="법원명 (예: 서울중앙지방법원)",
    )
    # 선택적 positional argument: 사건번호 (기본값: 2022타경3944)
    parser.add_argument(
        "csNo",
        nargs="?",
        default="2022타경3944",
        metavar="csNo",
        help="사건번호 (예: 2022타경3944)",
    )
    # 옵션 인자: 가져올 정보 탭, -t 또는 --tab 사용 가능 (기본값: 기일내역)
    parser.add_argument(
        "-t",
        "--tab",
        default="기일내역",
        choices=["사건내역", "기일내역", "문건/송달내역"],
        help="가져올 정보 탭 (기본값: 기일내역)",
    )
    args = parser.parse_args()
    result = main(args.court, args.csNo, args.tab)
    print(json.dumps(result, indent=2, ensure_ascii=False))