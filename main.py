"""
법원 경매 정보 요청 스크립트

이 스크립트는 지정된 법원 및 사건번호에 대해 웹 요청을 통해 경매 정보를 가져옵니다.
명령행 인자로 법원명, 사건번호(형식: "2022타경3944"), 그리고 가져올 정보 탭을 전달할 수 있으며,
기본값은 각각 "서울중앙지방법원", "2022타경3944", "기일내역"입니다.
"""

import json
import requests

# 법원명과 해당 법원 코드를 매핑하는 딕셔너리
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
    "제주지방법원": "B000530",
}

# 탭에 따른 요청 URL 매핑
URL_LIST = {
    "사건내역": "https://www.courtauction.go.kr/pgj/pgj15A/selectAuctnCsSrchRslt.on",
    "기일내역": "https://www.courtauction.go.kr/pgj/pgj15A/selectCsDtlDxdyDts.on",
    "문건/송달내역": "https://www.courtauction.go.kr/pgj/pgj15A/selectDlvrOfdocDtsDtl.on",
}

# 탭에 따른 페이로드 키 매핑
PAYLOAD_LIST = {
    "사건내역": "dma_srchCsDtlInf",
    "기일내역": "dma_srchDxdyDtsLst",
    "문건/송달내역": "dma_srchDlvrOfdocDts",
}


def main(court, cs_no, tab):
    """
    법원 경매 정보를 요청하는 메인 함수

    :param court: 법원명 (예: '서울중앙지방법원')
    :param cs_no: 사건번호 (형식: '2022타경3944')
    :param tab: 가져올 정보 탭 (예: '기일내역')
    :return: 요청 결과 데이터 (dict), 오류 발생 시 None 반환
    """
    # 사건번호를 앞자리와 뒷자리로 분리
    cs_no1, cs_no2 = cs_no.split("타경")
    cs_no2 = cs_no2.zfill(6)

    # 브라우저처럼 보이도록 HTTP 헤더 설정
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

    # 초기 페이지 요청으로 쿠키 획득
    initial_url = "https://www.courtauction.go.kr/pgj/index.on"
    session = requests.Session()
    response = session.get(initial_url, headers=headers)
    # 디버그용: 초기 GET 요청 상태를 출력 (필요 시 주석 해제)
    # print(f"Initial GET status: {response.status_code}".center(50, "-"))

    # Referer 헤더 추가 (보안 정책 우회를 위해 필요)
    headers.update({"Referer": initial_url})

    # POST 요청 URL과 페이로드 구성
    post_url = URL_LIST[tab]
    payload = {
        PAYLOAD_LIST[tab]: {
            "cortOfcCd": COURT_CODES[court],
            "csNo": f"{cs_no1}0130{cs_no2}",
        },
    }
    # "문건/송달내역" 탭인 경우 추가 파라미터 설정
    if tab == "문건/송달내역":
        payload[PAYLOAD_LIST[tab]].update({"srchFlag": "F"})

    # POST 요청 전송
    response = session.post(post_url, json=payload, headers=headers)
    # 디버그용: POST 응답 상태 출력 (필요 시 주석 해제)
    # print("POST response:".center(50, "-"))

    # 응답 JSON 파싱 및 데이터 반환
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