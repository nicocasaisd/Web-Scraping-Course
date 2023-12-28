from scrapy import Request

request_with_cookies = Request(
    url="https://urbania.pe/buscar/proyectos-propiedades?page=1", 
    cookies={
        "__cf_bm":"kunSsznaGNvoYtaoxD01egTvzCaf5LE.OJizF.gKMUs-1701910394-0-AXZBmomethFZ+nkY9z3Mppr8IVueXr5rbqO9H2EmK9gSK/f4Fn2NeAEtYoABs/zt0DF6mAKHwonp5SATnR/SctfGSdCELuFdTOsqKr8eqINN",
        "cf_chl_2":"0effd2c80e833bd",
        "cf_clearance":"52NF8kO94KRIdcUShPGrK.ufenUI_.yVmlCZYUgIUFY-1701907260-0-1-4ffdecad.e14b9ce0.18fcb34d-250.2.1701907260",
        "JSESSIONID":"076C94FF9EC2A5E8182DB73AB19E3ACE",
        "sessionId":"188d6dad-49f6-4364-be07-5e99427da96b",
        "g_state":'{"i_p":1701914466197,"i_l":1}',
        "idUltimoAvisoVisto":"64415011",
        "allowCookies":"true"
    }
)

print(request_with_cookies.headers)