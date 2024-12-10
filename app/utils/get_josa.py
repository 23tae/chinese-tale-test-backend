def get_josa(word, josa_pairs):
    """
    한국어 단어의 받침 유무에 따라 적절한 조사를 반환합니다.

    Args:
        word (str): 검사할 단어
        josa_pairs (tuple): (받침 있을 때 조사, 받침 없을 때 조사)

    Returns:
        str: 적절한 조사
    """
    if not word:
        return josa_pairs[0]

    # 한글 유니코드 범위 내에서 받침 확인
    UNICODE_N = ord('가')
    char_code = ord(word[-1]) - UNICODE_N

    # 받침 있음(1) / 없음(0)
    has_jongseong = bool(char_code % 28)

    return josa_pairs[0] if has_jongseong else josa_pairs[1]