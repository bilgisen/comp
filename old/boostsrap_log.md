2026-06-27 23:02:59,553 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ICBCT&exchange=TRY&financialGroup=UFRS_K&_=1782590578769&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ICBCT: 192 items, 786ms'
Arguments: ()
2026-06-27 23:02:59,558 - services.isyatirim_client - INFO - ✅ Successfully fetched ICBCT: 192 items, 786ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ICBCT: 768 rows, 786ms (23/57)'
Arguments: ()
2026-06-27 23:03:00,520 - __main__ - INFO - ✅ ICBCT: 768 rows, 786ms (23/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ICUGS mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:07,018 - services.isyatirim_client - INFO - 📥 Fetching ICUGS mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:07,347 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ICUGS&exchange=TRY&financialGroup=UFRS_K&_=1782590587018&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ICUGS - no financial data available'
Arguments: ()
2026-06-27 23:03:07,350 - services.isyatirim_client - WARNING - ⚠️ Empty response for ICUGS - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ICUGS: 0 items, 331ms'
Arguments: ()
2026-06-27 23:03:07,355 - services.isyatirim_client - INFO - ✅ Successfully fetched ICUGS: 0 items, 331ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ICUGS: 0 rows, 331ms (24/57)'
Arguments: ()
2026-06-27 23:03:08,123 - __main__ - INFO - ✅ ICUGS: 0 rows, 331ms (24/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching INFO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:14,200 - services.isyatirim_client - INFO - 📥 Fetching INFO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:14,550 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=INFO&exchange=TRY&financialGroup=UFRS_K&_=1782590594200&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for INFO - no financial data available'
Arguments: ()
2026-06-27 23:03:14,551 - services.isyatirim_client - WARNING - ⚠️ Empty response for INFO - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched INFO: 0 items, 350ms'
Arguments: ()
2026-06-27 23:03:14,556 - services.isyatirim_client - INFO - ✅ Successfully fetched INFO: 0 items, 350ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ INFO: 0 rows, 350ms (25/57)'
Arguments: ()
2026-06-27 23:03:14,997 - __main__ - INFO - ✅ INFO: 0 rows, 350ms (25/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISATR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:20,934 - services.isyatirim_client - INFO - 📥 Fetching ISATR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:24,395 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISATR&exchange=TRY&financialGroup=UFRS_K&_=1782590600934&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISATR: 192 items, 3462ms'
Arguments: ()
2026-06-27 23:03:24,398 - services.isyatirim_client - INFO - ✅ Successfully fetched ISATR: 192 items, 3462ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISATR: 768 rows, 3462ms (26/57)'
Arguments: ()
2026-06-27 23:03:25,381 - __main__ - INFO - ✅ ISATR: 768 rows, 3462ms (26/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISBTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:31,703 - services.isyatirim_client - INFO - 📥 Fetching ISBTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:32,735 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISBTR&exchange=TRY&financialGroup=UFRS_K&_=1782590611703&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISBTR: 192 items, 1041ms'
Arguments: ()
2026-06-27 23:03:32,746 - services.isyatirim_client - INFO - ✅ Successfully fetched ISBTR: 192 items, 1041ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISBTR: 768 rows, 1041ms (27/57)'
Arguments: ()
2026-06-27 23:03:33,659 - __main__ - INFO - ✅ ISBTR: 768 rows, 1041ms (27/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISCTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:39,304 - services.isyatirim_client - INFO - 📥 Fetching ISCTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:42,751 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISCTR&exchange=TRY&financialGroup=UFRS_K&_=1782590619304&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISCTR: 192 items, 3821ms'
Arguments: ()
2026-06-27 23:03:43,127 - services.isyatirim_client - INFO - ✅ Successfully fetched ISCTR: 192 items, 3821ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISCTR: 768 rows, 3821ms (28/57)'
Arguments: ()
2026-06-27 23:03:44,333 - __main__ - INFO - ✅ ISCTR: 768 rows, 3821ms (28/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISFIN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:50,638 - services.isyatirim_client - INFO - 📥 Fetching ISFIN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:51,270 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISFIN&exchange=TRY&financialGroup=UFRS_K&_=1782590630638&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ISFIN - no financial data available'
Arguments: ()
2026-06-27 23:03:51,271 - services.isyatirim_client - WARNING - ⚠️ Empty response for ISFIN - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISFIN: 0 items, 633ms'
Arguments: ()
2026-06-27 23:03:51,286 - services.isyatirim_client - INFO - ✅ Successfully fetched ISFIN: 0 items, 633ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISFIN: 0 rows, 633ms (29/57)'
Arguments: ()
2026-06-27 23:03:51,742 - __main__ - INFO - ✅ ISFIN: 0 rows, 633ms (29/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISGSY mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:03:57,473 - services.isyatirim_client - INFO - 📥 Fetching ISGSY mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:03:57,861 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISGSY&exchange=TRY&financialGroup=UFRS_K&_=1782590637473&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ISGSY - no financial data available'
Arguments: ()
2026-06-27 23:03:57,862 - services.isyatirim_client - WARNING - ⚠️ Empty response for ISGSY - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISGSY: 0 items, 388ms'
Arguments: ()
2026-06-27 23:03:57,874 - services.isyatirim_client - INFO - ✅ Successfully fetched ISGSY: 0 items, 388ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISGSY: 0 rows, 388ms (30/57)'
Arguments: ()
2026-06-27 23:03:58,657 - __main__ - INFO - ✅ ISGSY: 0 rows, 388ms (30/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISKUR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:04,270 - services.isyatirim_client - INFO - 📥 Fetching ISKUR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:04,653 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISKUR&exchange=TRY&financialGroup=UFRS_K&_=1782590644270&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ISKUR - no financial data available'
Arguments: ()
2026-06-27 23:04:04,654 - services.isyatirim_client - WARNING - ⚠️ Empty response for ISKUR - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISKUR: 0 items, 383ms'
Arguments: ()
2026-06-27 23:04:04,659 - services.isyatirim_client - INFO - ✅ Successfully fetched ISKUR: 0 items, 383ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISKUR: 0 rows, 383ms (31/57)'
Arguments: ()
2026-06-27 23:04:05,100 - __main__ - INFO - ✅ ISKUR: 0 rows, 383ms (31/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISMEN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:11,169 - services.isyatirim_client - INFO - 📥 Fetching ISMEN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:11,952 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISMEN&exchange=TRY&financialGroup=UFRS_K&_=1782590651169&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ISMEN - no financial data available'
Arguments: ()
2026-06-27 23:04:11,953 - services.isyatirim_client - WARNING - ⚠️ Empty response for ISMEN - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISMEN: 0 items, 783ms'
Arguments: ()
2026-06-27 23:04:11,966 - services.isyatirim_client - INFO - ✅ Successfully fetched ISMEN: 0 items, 783ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISMEN: 0 rows, 783ms (32/57)'
Arguments: ()
2026-06-27 23:04:12,733 - __main__ - INFO - ✅ ISMEN: 0 rows, 783ms (32/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ISYAT mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:18,421 - services.isyatirim_client - INFO - 📥 Fetching ISYAT mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:18,741 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ISYAT&exchange=TRY&financialGroup=UFRS_K&_=1782590658421&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ISYAT - no financial data available'
Arguments: ()
2026-06-27 23:04:18,742 - services.isyatirim_client - WARNING - ⚠️ Empty response for ISYAT - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ISYAT: 0 items, 321ms'
Arguments: ()
2026-06-27 23:04:18,748 - services.isyatirim_client - INFO - ✅ Successfully fetched ISYAT: 0 items, 321ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ISYAT: 0 rows, 321ms (33/57)'
Arguments: ()
2026-06-27 23:04:19,189 - __main__ - INFO - ✅ ISYAT: 0 rows, 321ms (33/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching KLNMA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:25,333 - services.isyatirim_client - INFO - 📥 Fetching KLNMA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:25,726 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=KLNMA&exchange=TRY&financialGroup=UFRS_K&_=1782590665333&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched KLNMA: 192 items, 395ms'
Arguments: ()
2026-06-27 23:04:25,729 - services.isyatirim_client - INFO - ✅ Successfully fetched KLNMA: 192 items, 395ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ KLNMA: 768 rows, 395ms (34/57)'
Arguments: ()
2026-06-27 23:04:26,626 - __main__ - INFO - ✅ KLNMA: 768 rows, 395ms (34/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching LIDFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:32,216 - services.isyatirim_client - INFO - 📥 Fetching LIDFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:32,524 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=LIDFA&exchange=TRY&financialGroup=UFRS_K&_=1782590672216&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for LIDFA - no financial data available'
Arguments: ()
2026-06-27 23:04:32,525 - services.isyatirim_client - WARNING - ⚠️ Empty response for LIDFA - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched LIDFA: 0 items, 309ms'
Arguments: ()
2026-06-27 23:04:32,531 - services.isyatirim_client - INFO - ✅ Successfully fetched LIDFA: 0 items, 309ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ LIDFA: 0 rows, 309ms (35/57)'
Arguments: ()
2026-06-27 23:04:32,974 - __main__ - INFO - ✅ LIDFA: 0 rows, 309ms (35/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching MTRYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:38,903 - services.isyatirim_client - INFO - 📥 Fetching MTRYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:39,388 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=MTRYO&exchange=TRY&financialGroup=UFRS_K&_=1782590678903&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for MTRYO - no financial data available'
Arguments: ()
2026-06-27 23:04:39,389 - services.isyatirim_client - WARNING - ⚠️ Empty response for MTRYO - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched MTRYO: 0 items, 485ms'
Arguments: ()
2026-06-27 23:04:39,398 - services.isyatirim_client - INFO - ✅ Successfully fetched MTRYO: 0 items, 485ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ MTRYO: 0 rows, 485ms (36/57)'
Arguments: ()
2026-06-27 23:04:39,838 - __main__ - INFO - ✅ MTRYO: 0 rows, 485ms (36/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching OSMEN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:45,617 - services.isyatirim_client - INFO - 📥 Fetching OSMEN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:46,378 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=OSMEN&exchange=TRY&financialGroup=UFRS_K&_=1782590685617&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for OSMEN - no financial data available'
Arguments: ()
2026-06-27 23:04:46,379 - services.isyatirim_client - WARNING - ⚠️ Empty response for OSMEN - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched OSMEN: 0 items, 761ms'
Arguments: ()
2026-06-27 23:04:46,385 - services.isyatirim_client - INFO - ✅ Successfully fetched OSMEN: 0 items, 761ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ OSMEN: 0 rows, 761ms (37/57)'
Arguments: ()
2026-06-27 23:04:46,825 - __main__ - INFO - ✅ OSMEN: 0 rows, 761ms (37/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching OYAYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:52,606 - services.isyatirim_client - INFO - 📥 Fetching OYAYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:04:53,017 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=OYAYO&exchange=TRY&financialGroup=UFRS_K&_=1782590692606&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for OYAYO - no financial data available'
Arguments: ()
2026-06-27 23:04:53,020 - services.isyatirim_client - WARNING - ⚠️ Empty response for OYAYO - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched OYAYO: 0 items, 414ms'
Arguments: ()
2026-06-27 23:04:53,025 - services.isyatirim_client - INFO - ✅ Successfully fetched OYAYO: 0 items, 414ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ OYAYO: 0 rows, 414ms (38/57)'
Arguments: ()
2026-06-27 23:04:53,468 - __main__ - INFO - ✅ OYAYO: 0 rows, 414ms (38/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching OYYAT mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:04:59,903 - services.isyatirim_client - INFO - 📥 Fetching OYYAT mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:00,230 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=OYYAT&exchange=TRY&financialGroup=UFRS_K&_=1782590699903&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for OYYAT - no financial data available'
Arguments: ()
2026-06-27 23:05:00,231 - services.isyatirim_client - WARNING - ⚠️ Empty response for OYYAT - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched OYYAT: 0 items, 328ms'
Arguments: ()
2026-06-27 23:05:00,237 - services.isyatirim_client - INFO - ✅ Successfully fetched OYYAT: 0 items, 328ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ OYYAT: 0 rows, 328ms (39/57)'
Arguments: ()
2026-06-27 23:05:00,678 - __main__ - INFO - ✅ OYYAT: 0 rows, 328ms (39/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching PRDGS mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:06,304 - services.isyatirim_client - INFO - 📥 Fetching PRDGS mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:06,710 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=PRDGS&exchange=TRY&financialGroup=UFRS_K&_=1782590706304&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for PRDGS - no financial data available'
Arguments: ()
2026-06-27 23:05:06,712 - services.isyatirim_client - WARNING - ⚠️ Empty response for PRDGS - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched PRDGS: 0 items, 406ms'
Arguments: ()
2026-06-27 23:05:06,717 - services.isyatirim_client - INFO - ✅ Successfully fetched PRDGS: 0 items, 406ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ PRDGS: 0 rows, 406ms (40/57)'
Arguments: ()
2026-06-27 23:05:08,070 - __main__ - INFO - ✅ PRDGS: 0 rows, 406ms (40/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching QNBFK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:14,116 - services.isyatirim_client - INFO - 📥 Fetching QNBFK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:14,489 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=QNBFK&exchange=TRY&financialGroup=UFRS_K&_=1782590714116&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for QNBFK - no financial data available'
Arguments: ()
2026-06-27 23:05:14,490 - services.isyatirim_client - WARNING - ⚠️ Empty response for QNBFK - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched QNBFK: 0 items, 373ms'
Arguments: ()
2026-06-27 23:05:14,497 - services.isyatirim_client - INFO - ✅ Successfully fetched QNBFK: 0 items, 373ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ QNBFK: 0 rows, 373ms (41/57)'
Arguments: ()
2026-06-27 23:05:14,940 - __main__ - INFO - ✅ QNBFK: 0 rows, 373ms (41/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching QNBTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:20,836 - services.isyatirim_client - INFO - 📥 Fetching QNBTR mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:21,234 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=QNBTR&exchange=TRY&financialGroup=UFRS_K&_=1782590720836&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched QNBTR: 192 items, 400ms'
Arguments: ()
2026-06-27 23:05:21,237 - services.isyatirim_client - INFO - ✅ Successfully fetched QNBTR: 192 items, 400ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ QNBTR: 768 rows, 400ms (42/57)'
Arguments: ()
2026-06-27 23:05:22,337 - __main__ - INFO - ✅ QNBTR: 768 rows, 400ms (42/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching SEKFK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:28,640 - services.isyatirim_client - INFO - 📥 Fetching SEKFK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:30,244 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=SEKFK&exchange=TRY&financialGroup=UFRS_K&_=1782590728640&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for SEKFK - no financial data available'
Arguments: ()
2026-06-27 23:05:30,246 - services.isyatirim_client - WARNING - ⚠️ Empty response for SEKFK - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched SEKFK: 0 items, 1605ms'
Arguments: ()
2026-06-27 23:05:30,251 - services.isyatirim_client - INFO - ✅ Successfully fetched SEKFK: 0 items, 1605ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ SEKFK: 0 rows, 1605ms (43/57)'
Arguments: ()
2026-06-27 23:05:30,691 - __main__ - INFO - ✅ SEKFK: 0 rows, 1605ms (43/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching SKBNK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:36,334 - services.isyatirim_client - INFO - 📥 Fetching SKBNK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:36,724 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=SKBNK&exchange=TRY&financialGroup=UFRS_K&_=1782590736334&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched SKBNK: 192 items, 392ms'
Arguments: ()
2026-06-27 23:05:36,728 - services.isyatirim_client - INFO - ✅ Successfully fetched SKBNK: 192 items, 392ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ SKBNK: 768 rows, 392ms (44/57)'
Arguments: ()
2026-06-27 23:05:38,538 - __main__ - INFO - ✅ SKBNK: 768 rows, 392ms (44/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching SKYMD mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:45,038 - services.isyatirim_client - INFO - 📥 Fetching SKYMD mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:45,353 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=SKYMD&exchange=TRY&financialGroup=UFRS_K&_=1782590745038&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for SKYMD - no financial data available'
Arguments: ()
2026-06-27 23:05:45,354 - services.isyatirim_client - WARNING - ⚠️ Empty response for SKYMD - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched SKYMD: 0 items, 316ms'
Arguments: ()
2026-06-27 23:05:45,360 - services.isyatirim_client - INFO - ✅ Successfully fetched SKYMD: 0 items, 316ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ SKYMD: 0 rows, 316ms (45/57)'
Arguments: ()
2026-06-27 23:05:46,130 - __main__ - INFO - ✅ SKYMD: 0 rows, 316ms (45/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching SMRVA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:05:52,205 - services.isyatirim_client - INFO - 📥 Fetching SMRVA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:05:55,634 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=SMRVA&exchange=TRY&financialGroup=UFRS_K&_=1782590752205&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for SMRVA - no financial data available'
Arguments: ()
2026-06-27 23:05:55,635 - services.isyatirim_client - WARNING - ⚠️ Empty response for SMRVA - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched SMRVA: 0 items, 3430ms'
Arguments: ()
2026-06-27 23:05:55,640 - services.isyatirim_client - INFO - ✅ Successfully fetched SMRVA: 0 items, 3430ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ SMRVA: 0 rows, 3430ms (46/57)'
Arguments: ()
2026-06-27 23:05:56,081 - __main__ - INFO - ✅ SMRVA: 0 rows, 3430ms (46/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching TERA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:06:02,104 - services.isyatirim_client - INFO - 📥 Fetching TERA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:06:02,526 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=TERA&exchange=TRY&financialGroup=UFRS_K&_=1782590762104&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for TERA - no financial data available'
Arguments: ()
2026-06-27 23:06:02,527 - services.isyatirim_client - WARNING - ⚠️ Empty response for TERA - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched TERA: 0 items, 423ms'
Arguments: ()
2026-06-27 23:06:02,533 - services.isyatirim_client - INFO - ✅ Successfully fetched TERA: 0 items, 423ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ TERA: 0 rows, 423ms (47/57)'
Arguments: ()
2026-06-27 23:06:03,301 - __main__ - INFO - ✅ TERA: 0 rows, 423ms (47/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching TSKB mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:06:09,570 - services.isyatirim_client - INFO - 📥 Fetching TSKB mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:06:10,260 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=TSKB&exchange=TRY&financialGroup=UFRS_K&_=1782590769570&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched TSKB: 192 items, 751ms'
Arguments: ()
2026-06-27 23:06:10,323 - services.isyatirim_client - INFO - ✅ Successfully fetched TSKB: 192 items, 751ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ TSKB: 768 rows, 751ms (48/57)'
Arguments: ()
2026-06-27 23:06:12,335 - __main__ - INFO - ✅ TSKB: 768 rows, 751ms (48/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching UFUK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:06:18,639 - services.isyatirim_client - INFO - 📥 Fetching UFUK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:06:19,028 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=UFUK&exchange=TRY&financialGroup=UFRS_K&_=1782590778639&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for UFUK - no financial data available'
Arguments: ()
2026-06-27 23:06:19,029 - services.isyatirim_client - WARNING - ⚠️ Empty response for UFUK - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched UFUK: 0 items, 390ms'
Arguments: ()
2026-06-27 23:06:19,035 - services.isyatirim_client - INFO - ✅ Successfully fetched UFUK: 0 items, 390ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ UFUK: 0 rows, 390ms (49/57)'
Arguments: ()
2026-06-27 23:06:19,478 - __main__ - INFO - ✅ UFUK: 0 rows, 390ms (49/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching ULUFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:06:25,897 - services.isyatirim_client - INFO - 📥 Fetching ULUFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:06:26,214 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=ULUFA&exchange=TRY&financialGroup=UFRS_K&_=1782590785897&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for ULUFA - no financial data available'
Arguments: ()
2026-06-27 23:06:26,215 - services.isyatirim_client - WARNING - ⚠️ Empty response for ULUFA - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched ULUFA: 0 items, 317ms'
Arguments: ()
2026-06-27 23:06:26,221 - services.isyatirim_client - INFO - ✅ Successfully fetched ULUFA: 0 items, 317ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ ULUFA: 0 rows, 317ms (50/57)'
Arguments: ()
2026-06-27 23:06:26,659 - __main__ - INFO - ✅ ULUFA: 0 rows, 317ms (50/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 184, in _phase_fetch
    async with isyatirim_client:
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 95, in __aexit__
    await self.disconnect()
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 118, in disconnect
    logger.info("✅ İş Yatırım API client closed")
Message: '✅ İş Yatırım API client closed'
Arguments: ()
2026-06-27 23:06:29,667 - services.isyatirim_client - INFO - ✅ İş Yatırım API client closed
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f634' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 223, in _phase_fetch
    logger.info(f"😴 Session break: {self.SESSION_BREAK}s")
Message: '😴 Session break: 120s'
Arguments: ()
2026-06-27 23:06:29,673 - __main__ - INFO - 😴 Session break: 120s
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e6' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 182, in _phase_fetch
    logger.info(f"📦 Batch {batch_num}/{total_batches}: {len(batch)} companies")
Message: '📦 Batch 2/2: 7 companies'
Arguments: ()
2026-06-27 23:08:29,674 - __main__ - INFO - 📦 Batch 2/2: 7 companies
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 184, in _phase_fetch
    async with isyatirim_client:
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 90, in __aenter__
    await self.connect()
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 111, in connect
    logger.info("✅ İş Yatırım API client initialized")
Message: '✅ İş Yatırım API client initialized'
Arguments: ()
2026-06-27 23:08:30,022 - services.isyatirim_client - INFO - ✅ İş Yatırım API client initialized
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching UNLU mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:08:32,987 - services.isyatirim_client - INFO - 📥 Fetching UNLU mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:08:33,366 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=UNLU&exchange=TRY&financialGroup=UFRS_K&_=1782590912987&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for UNLU - no financial data available'
Arguments: ()
2026-06-27 23:08:33,368 - services.isyatirim_client - WARNING - ⚠️ Empty response for UNLU - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched UNLU: 0 items, 381ms'
Arguments: ()
2026-06-27 23:08:33,373 - services.isyatirim_client - INFO - ✅ Successfully fetched UNLU: 0 items, 381ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ UNLU: 0 rows, 381ms (51/57)'
Arguments: ()
2026-06-27 23:08:33,817 - __main__ - INFO - ✅ UNLU: 0 rows, 381ms (51/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching VAKBN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:08:39,607 - services.isyatirim_client - INFO - 📥 Fetching VAKBN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:08:40,025 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=VAKBN&exchange=TRY&financialGroup=UFRS_K&_=1782590919607&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched VAKBN: 192 items, 420ms'
Arguments: ()
2026-06-27 23:08:40,029 - services.isyatirim_client - INFO - ✅ Successfully fetched VAKBN: 192 items, 420ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ VAKBN: 768 rows, 420ms (52/57)'
Arguments: ()
2026-06-27 23:08:41,028 - __main__ - INFO - ✅ VAKBN: 768 rows, 420ms (52/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching VAKFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:08:47,023 - services.isyatirim_client - INFO - 📥 Fetching VAKFA mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:08:50,446 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=VAKFA&exchange=TRY&financialGroup=UFRS_K&_=1782590927023&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for VAKFA - no financial data available'
Arguments: ()
2026-06-27 23:08:50,448 - services.isyatirim_client - WARNING - ⚠️ Empty response for VAKFA - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched VAKFA: 0 items, 3425ms'
Arguments: ()
2026-06-27 23:08:50,453 - services.isyatirim_client - INFO - ✅ Successfully fetched VAKFA: 0 items, 3425ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ VAKFA: 0 rows, 3425ms (53/57)'
Arguments: ()
2026-06-27 23:08:50,894 - __main__ - INFO - ✅ VAKFA: 0 rows, 3425ms (53/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching VAKFN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:08:56,734 - services.isyatirim_client - INFO - 📥 Fetching VAKFN mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:08:57,052 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=VAKFN&exchange=TRY&financialGroup=UFRS_K&_=1782590936734&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for VAKFN - no financial data available'
Arguments: ()
2026-06-27 23:08:57,054 - services.isyatirim_client - WARNING - ⚠️ Empty response for VAKFN - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched VAKFN: 0 items, 320ms'
Arguments: ()
2026-06-27 23:08:57,060 - services.isyatirim_client - INFO - ✅ Successfully fetched VAKFN: 0 items, 320ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ VAKFN: 0 rows, 320ms (54/57)'
Arguments: ()
2026-06-27 23:08:57,502 - __main__ - INFO - ✅ VAKFN: 0 rows, 320ms (54/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching VERTU mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:09:03,952 - services.isyatirim_client - INFO - 📥 Fetching VERTU mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:09:05,369 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=VERTU&exchange=TRY&financialGroup=UFRS_K&_=1782590943952&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for VERTU - no financial data available'
Arguments: ()
2026-06-27 23:09:05,371 - services.isyatirim_client - WARNING - ⚠️ Empty response for VERTU - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched VERTU: 0 items, 1418ms'
Arguments: ()
2026-06-27 23:09:05,376 - services.isyatirim_client - INFO - ✅ Successfully fetched VERTU: 0 items, 1418ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ VERTU: 0 rows, 1418ms (55/57)'
Arguments: ()
2026-06-27 23:09:05,820 - __main__ - INFO - ✅ VERTU: 0 rows, 1418ms (55/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching VKFYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:09:11,581 - services.isyatirim_client - INFO - 📥 Fetching VKFYO mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:09:11,905 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=VKFYO&exchange=TRY&financialGroup=UFRS_K&_=1782590951581&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 64-65: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 291, in fetch_mali_tablo
    logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
Message: '⚠️ Empty response for VKFYO - no financial data available'
Arguments: ()
2026-06-27 23:09:11,906 - services.isyatirim_client - WARNING - ⚠️ Empty response for VKFYO - no financial data available
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched VKFYO: 0 items, 324ms'
Arguments: ()
2026-06-27 23:09:11,914 - services.isyatirim_client - INFO - ✅ Successfully fetched VKFYO: 0 items, 324ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ VKFYO: 0 rows, 324ms (56/57)'
Arguments: ()
2026-06-27 23:09:12,356 - __main__ - INFO - ✅ VKFYO: 0 rows, 324ms (56/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 222, in fetch_mali_tablo
    logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
Message: '📥 Fetching YKBNK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]'
Arguments: ()
2026-06-27 23:09:18,679 - services.isyatirim_client - INFO - 📥 Fetching YKBNK mali tablo for periods [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]
2026-06-27 23:09:22,126 - httpx - INFO - HTTP Request: GET https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=YKBNK&exchange=TRY&financialGroup=UFRS_K&_=1782590958679&year1=2026&period1=3&year2=2025&period2=12&year3=2025&period3=9&year4=2025&period4=6 "HTTP/1.1 200 OK"
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 195, in _phase_fetch
    result = await self._fetch_company(ticker, company.financial_group)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 372, in _fetch_company
    result = await isyatirim_client.fetch_mali_tablo(
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 295, in fetch_mali_tablo
    logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
Message: '✅ Successfully fetched YKBNK: 192 items, 3449ms'
Arguments: ()
2026-06-27 23:09:22,130 - services.isyatirim_client - INFO - ✅ Successfully fetched YKBNK: 192 items, 3449ms
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 202, in _phase_fetch
    logger.info(
Message: '✅ YKBNK: 768 rows, 3449ms (57/57)'
Arguments: ()
2026-06-27 23:09:23,671 - __main__ - INFO - ✅ YKBNK: 768 rows, 3449ms (57/57)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 61: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 184, in _phase_fetch
    async with isyatirim_client:
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 95, in __aexit__
    await self.disconnect()
  File "C:\Users\ASUS\hp\comp\services\isyatirim_client.py", line 118, in disconnect
    logger.info("✅ İş Yatırım API client closed")
Message: '✅ İş Yatırım API client closed'
Arguments: ()
2026-06-27 23:09:26,690 - services.isyatirim_client - INFO - ✅ İş Yatırım API client closed
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 124, in run
    await self._phase_fetch()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 226, in _phase_fetch
    logger.info(f"✅ Fetch phase complete: {self.stats.successful_fetches} successful, {self.stats.failed_fetches} failed")
Message: '✅ Fetch phase complete: 57 successful, 0 failed'
Arguments: ()
2026-06-27 23:09:26,696 - __main__ - INFO - ✅ Fetch phase complete: 57 successful, 0 failed
2026-06-27 23:09:26,698 - __main__ - INFO - ============================================================
2026-06-27 23:09:26,698 - __main__ - INFO - PHASE 2: RATIO CALCULATION
2026-06-27 23:09:26,698 - __main__ - INFO - ============================================================
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 132, in run
    await self._phase_calculate_ratios()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 238, in _phase_calculate_ratios
    logger.info(f"🧮 Calculating ratios for {len(companies_with_data)} companies")
Message: '🧮 Calculating ratios for 27 companies'
Arguments: ()
2026-06-27 23:09:27,139 - __main__ - INFO - 🧮 Calculating ratios for 27 companies
2026-06-27 23:09:27,930 - services.ratio_calculator - ERROR - Error getting financial data for AKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:28,373 - services.ratio_calculator - ERROR - Error getting financial data for AKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:28,815 - services.ratio_calculator - ERROR - Error getting financial data for AKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:29,254 - services.ratio_calculator - ERROR - Error getting financial data for AKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:30,447 - services.ratio_calculator - ERROR - Error getting financial data for AKCNS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:30,890 - services.ratio_calculator - ERROR - Error getting financial data for AKCNS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:31,329 - services.ratio_calculator - ERROR - Error getting financial data for AKCNS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:31,770 - services.ratio_calculator - ERROR - Error getting financial data for AKCNS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:32,645 - services.ratio_calculator - ERROR - Error getting financial data for ALBRK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:33,088 - services.ratio_calculator - ERROR - Error getting financial data for ALBRK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:33,528 - services.ratio_calculator - ERROR - Error getting financial data for ALBRK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:33,971 - services.ratio_calculator - ERROR - Error getting financial data for ALBRK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:35,165 - services.ratio_calculator - ERROR - Error getting financial data for ASELS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:35,919 - services.ratio_calculator - ERROR - Error getting financial data for ASELS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:36,362 - services.ratio_calculator - ERROR - Error getting financial data for ASELS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:36,805 - services.ratio_calculator - ERROR - Error getting financial data for ASELS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:37,684 - services.ratio_calculator - ERROR - Error getting financial data for CLEBI: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:38,441 - services.ratio_calculator - ERROR - Error getting financial data for CLEBI: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:38,883 - services.ratio_calculator - ERROR - Error getting financial data for CLEBI: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:39,324 - services.ratio_calculator - ERROR - Error getting financial data for CLEBI: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:40,206 - services.ratio_calculator - ERROR - Error getting financial data for EREGL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:40,962 - services.ratio_calculator - ERROR - Error getting financial data for EREGL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:41,402 - services.ratio_calculator - ERROR - Error getting financial data for EREGL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:42,154 - services.ratio_calculator - ERROR - Error getting financial data for EREGL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:43,033 - services.ratio_calculator - ERROR - Error getting financial data for FROTO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:43,475 - services.ratio_calculator - ERROR - Error getting financial data for FROTO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:43,917 - services.ratio_calculator - ERROR - Error getting financial data for FROTO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:44,672 - services.ratio_calculator - ERROR - Error getting financial data for FROTO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:45,554 - services.ratio_calculator - ERROR - Error getting financial data for GARAN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:45,995 - services.ratio_calculator - ERROR - Error getting financial data for GARAN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:46,438 - services.ratio_calculator - ERROR - Error getting financial data for GARAN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:46,878 - services.ratio_calculator - ERROR - Error getting financial data for GARAN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:47,758 - services.ratio_calculator - ERROR - Error getting financial data for HALKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:48,202 - services.ratio_calculator - ERROR - Error getting financial data for HALKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:48,644 - services.ratio_calculator - ERROR - Error getting financial data for HALKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:49,085 - services.ratio_calculator - ERROR - Error getting financial data for HALKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:50,284 - services.ratio_calculator - ERROR - Error getting financial data for ICBCT: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:51,352 - services.ratio_calculator - ERROR - Error getting financial data for ICBCT: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:52,107 - services.ratio_calculator - ERROR - Error getting financial data for ICBCT: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:52,552 - services.ratio_calculator - ERROR - Error getting financial data for ICBCT: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 132, in run
    await self._phase_calculate_ratios()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 300, in _phase_calculate_ratios
    logger.info(f"🧮 Progress: {processed_count}/{len(companies_with_data)} companies")
Message: '🧮 Progress: 10/27 companies'
Arguments: ()
2026-06-27 23:09:52,665 - __main__ - INFO - 🧮 Progress: 10/27 companies
2026-06-27 23:09:54,075 - services.ratio_calculator - ERROR - Error getting financial data for ISATR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:54,833 - services.ratio_calculator - ERROR - Error getting financial data for ISATR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:55,587 - services.ratio_calculator - ERROR - Error getting financial data for ISATR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:56,030 - services.ratio_calculator - ERROR - Error getting financial data for ISATR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:57,221 - services.ratio_calculator - ERROR - Error getting financial data for ISBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:57,664 - services.ratio_calculator - ERROR - Error getting financial data for ISBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:58,109 - services.ratio_calculator - ERROR - Error getting financial data for ISBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:58,550 - services.ratio_calculator - ERROR - Error getting financial data for ISBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:59,432 - services.ratio_calculator - ERROR - Error getting financial data for ISCTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:09:59,872 - services.ratio_calculator - ERROR - Error getting financial data for ISCTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:00,628 - services.ratio_calculator - ERROR - Error getting financial data for ISCTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:01,388 - services.ratio_calculator - ERROR - Error getting financial data for ISCTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:02,594 - services.ratio_calculator - ERROR - Error getting financial data for KCHOL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:03,352 - services.ratio_calculator - ERROR - Error getting financial data for KCHOL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:03,796 - services.ratio_calculator - ERROR - Error getting financial data for KCHOL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:35,230 - services.ratio_calculator - ERROR - Error getting financial data for KCHOL: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:36,406 - services.ratio_calculator - ERROR - Error getting financial data for KLNMA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:36,842 - services.ratio_calculator - ERROR - Error getting financial data for KLNMA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:37,275 - services.ratio_calculator - ERROR - Error getting financial data for KLNMA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:37,706 - services.ratio_calculator - ERROR - Error getting financial data for KLNMA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:39,188 - services.ratio_calculator - ERROR - Error getting financial data for KRDMD: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:39,933 - services.ratio_calculator - ERROR - Error getting financial data for KRDMD: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:40,365 - services.ratio_calculator - ERROR - Error getting financial data for KRDMD: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:40,799 - services.ratio_calculator - ERROR - Error getting financial data for KRDMD: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:41,662 - services.ratio_calculator - ERROR - Error getting financial data for PGSUS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:42,095 - services.ratio_calculator - ERROR - Error getting financial data for PGSUS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:42,529 - services.ratio_calculator - ERROR - Error getting financial data for PGSUS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:42,960 - services.ratio_calculator - ERROR - Error getting financial data for PGSUS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:43,822 - services.ratio_calculator - ERROR - Error getting financial data for QNBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:44,253 - services.ratio_calculator - ERROR - Error getting financial data for QNBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:44,685 - services.ratio_calculator - ERROR - Error getting financial data for QNBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:45,116 - services.ratio_calculator - ERROR - Error getting financial data for QNBTR: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:45,977 - services.ratio_calculator - ERROR - Error getting financial data for SASA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:46,718 - services.ratio_calculator - ERROR - Error getting financial data for SASA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:47,152 - services.ratio_calculator - ERROR - Error getting financial data for SASA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:47,894 - services.ratio_calculator - ERROR - Error getting financial data for SASA: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:49,061 - services.ratio_calculator - ERROR - Error getting financial data for SISE: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:49,808 - services.ratio_calculator - ERROR - Error getting financial data for SISE: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:50,550 - services.ratio_calculator - ERROR - Error getting financial data for SISE: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:50,980 - services.ratio_calculator - ERROR - Error getting financial data for SISE: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 132, in run
    await self._phase_calculate_ratios()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 300, in _phase_calculate_ratios
    logger.info(f"🧮 Progress: {processed_count}/{len(companies_with_data)} companies")
Message: '🧮 Progress: 20/27 companies'
Arguments: ()
2026-06-27 23:10:51,088 - __main__ - INFO - 🧮 Progress: 20/27 companies
2026-06-27 23:10:52,155 - services.ratio_calculator - ERROR - Error getting financial data for SKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:52,585 - services.ratio_calculator - ERROR - Error getting financial data for SKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:53,018 - services.ratio_calculator - ERROR - Error getting financial data for SKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:53,451 - services.ratio_calculator - ERROR - Error getting financial data for SKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:54,328 - services.ratio_calculator - ERROR - Error getting financial data for THYAO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:54,763 - services.ratio_calculator - ERROR - Error getting financial data for THYAO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:55,514 - services.ratio_calculator - ERROR - Error getting financial data for THYAO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:56,264 - services.ratio_calculator - ERROR - Error getting financial data for THYAO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:57,125 - services.ratio_calculator - ERROR - Error getting financial data for TOASO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:57,563 - services.ratio_calculator - ERROR - Error getting financial data for TOASO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:58,000 - services.ratio_calculator - ERROR - Error getting financial data for TOASO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:58,745 - services.ratio_calculator - ERROR - Error getting financial data for TOASO: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:10:59,920 - services.ratio_calculator - ERROR - Error getting financial data for TSKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:00,353 - services.ratio_calculator - ERROR - Error getting financial data for TSKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:00,789 - services.ratio_calculator - ERROR - Error getting financial data for TSKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:01,226 - services.ratio_calculator - ERROR - Error getting financial data for TSKB: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:02,092 - services.ratio_calculator - ERROR - Error getting financial data for TUPRS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:02,525 - services.ratio_calculator - ERROR - Error getting financial data for TUPRS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:02,956 - services.ratio_calculator - ERROR - Error getting financial data for TUPRS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:03,396 - services.ratio_calculator - ERROR - Error getting financial data for TUPRS: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:04,265 - services.ratio_calculator - ERROR - Error getting financial data for VAKBN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:04,699 - services.ratio_calculator - ERROR - Error getting financial data for VAKBN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:05,135 - services.ratio_calculator - ERROR - Error getting financial data for VAKBN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:05,570 - services.ratio_calculator - ERROR - Error getting financial data for VAKBN: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:06,741 - services.ratio_calculator - ERROR - Error getting financial data for YKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:07,174 - services.ratio_calculator - ERROR - Error getting financial data for YKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:07,606 - services.ratio_calculator - ERROR - Error getting financial data for YKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
2026-06-27 23:11:08,041 - services.ratio_calculator - ERROR - Error getting financial data for YKBNK: name 'Any' is not defined
Traceback (most recent call last):
  File "C:\Users\ASUS\hp\comp\services\ratio_calculator.py", line 379, in _get_financial_data
    from services.item_code_mapper import ItemCodeMapper
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 15, in <module>
    class ItemCodeMapper:
  File "C:\Users\ASUS\hp\comp\services\item_code_mapper.py", line 307, in ItemCodeMapper
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
                                                                                        ^^^
NameError: name 'Any' is not defined. Did you mean: 'any'?
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 132, in run
    await self._phase_calculate_ratios()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 307, in _phase_calculate_ratios
    logger.info(
Message: '✅ Ratio calculation complete: 0 ratios, 27 companies processed, 0 failed'
Arguments: ()
2026-06-27 23:11:08,148 - __main__ - INFO - ✅ Ratio calculation complete: 0 ratios, 27 companies processed, 0 failed
2026-06-27 23:11:08,154 - __main__ - INFO - ============================================================
2026-06-27 23:11:08,154 - __main__ - INFO - PHASE 3: SECTOR BENCHMARKS
2026-06-27 23:11:08,155 - __main__ - INFO - ============================================================
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 330, in _phase_calculate_benchmarks
    logger.info(f"📊 Calculating benchmarks for {len(sector_periods)} sector-period combinations")
Message: '📊 Calculating benchmarks for 6 sector-period combinations'
Arguments: ()
2026-06-27 23:11:10,853 - __main__ - INFO - 📊 Calculating benchmarks for 6 sector-period combinations
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Enerji (Üretim + Dağıtım + Petrol) 2026Q1'
Arguments: ()
2026-06-27 23:11:10,859 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Enerji (Üreti m + Dağıtım + Petrol) 2026Q1
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for acid_test_ratio: n=1'
Arguments: ()
2026-06-27 23:11:11,885 - services.sector_benchmarks - INFO - 📊 Insufficient peers for acid_test_ratio: n=1
2026-06-27 23:11:11,893 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for current_ratio: n=1'
Arguments: ()
2026-06-27 23:11:12,002 - services.sector_benchmarks - INFO - 📊 Insufficient peers for current_ratio: n=1
2026-06-27 23:11:12,008 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for debt_to_equity: n=1'
Arguments: ()
2026-06-27 23:11:12,117 - services.sector_benchmarks - INFO - 📊 Insufficient peers for debt_to_equity: n=1
2026-06-27 23:11:12,122 - services.sector_benchmarks - ERROR - Failed to compute debt_to_equity: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for net_debt_to_equity: n=0'
Arguments: ()
2026-06-27 23:11:12,229 - services.sector_benchmarks - INFO - 📊 Insufficient peers for net_debt_to_equity: n=0
2026-06-27 23:11:12,235 - services.sector_benchmarks - ERROR - Failed to compute net_debt_to_equity: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for pb_ratio: n=1'
Arguments: ()
2026-06-27 23:11:12,344 - services.sector_benchmarks - INFO - 📊 Insufficient peers for pb_ratio: n=1
2026-06-27 23:11:12,350 - services.sector_benchmarks - ERROR - Failed to compute pb_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for pe_ratio: n=1'
Arguments: ()
2026-06-27 23:11:12,459 - services.sector_benchmarks - INFO - 📊 Insufficient peers for pe_ratio: n=1
2026-06-27 23:11:12,539 - services.sector_benchmarks - ERROR - Failed to compute pe_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for receivables_turnover: n=0'
Arguments: ()
2026-06-27 23:11:12,649 - services.sector_benchmarks - INFO - 📊 Insufficient peers for receivables_turnover: n=0
2026-06-27 23:11:12,655 - services.sector_benchmarks - ERROR - Failed to compute receivables_turnover: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for roe: n=1'
Arguments: ()
2026-06-27 23:11:12,763 - services.sector_benchmarks - INFO - 📊 Insufficient peers for roe: n=1
2026-06-27 23:11:12,769 - services.sector_benchmarks - ERROR - Failed to compute roe: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/8 ratios'
Arguments: ()
2026-06-27 23:11:12,769 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/8 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Enerji (Üretim + Dağıtım + Petrol) 2026Q1: 0 benchmarks (1/6)'
Arguments: ()
2026-06-27 23:11:12,771 - __main__ - INFO - ✅ Enerji (Üretim + Dağıtım + Petrol) 2026Q1: 0 benchmarks (1/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Holdingler 2026Q1'
Arguments: ()
2026-06-27 23:11:12,883 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Holdingler 20 26Q1
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for acid_test_ratio: n=1'
Arguments: ()
2026-06-27 23:11:13,849 - services.sector_benchmarks - INFO - 📊 Insufficient peers for acid_test_ratio: n=1
2026-06-27 23:11:13,856 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for current_ratio: n=1'
Arguments: ()
2026-06-27 23:11:13,964 - services.sector_benchmarks - INFO - 📊 Insufficient peers for current_ratio: n=1
2026-06-27 23:11:13,970 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for roe: n=1'
Arguments: ()
2026-06-27 23:11:14,397 - services.sector_benchmarks - INFO - 📊 Insufficient peers for roe: n=1
2026-06-27 23:11:14,403 - services.sector_benchmarks - ERROR - Failed to compute roe: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/3 ratios'
Arguments: ()
2026-06-27 23:11:14,403 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/3 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Holdingler 2026Q1: 0 benchmarks (2/6)'
Arguments: ()
2026-06-27 23:11:14,405 - __main__ - INFO - ✅ Holdingler 2026Q1: 0 benchmarks (2/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Otomotiv & Savunma & Makine 2026Q1'
Arguments: ()
2026-06-27 23:11:14,514 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Otomotiv & Sa vunma & Makine 2026Q1
2026-06-27 23:11:16,030 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "uq_benchmark_peers_id_ticker"
DETAIL:  Key (benchmark_id, ticker)=(9, ASELS) already exists.
[SQL: INSERT INTO sector_benchmark_peers (benchmark_id, ticker, ratio_value, is_included) VALUES ($1::INTEGER, $2::VARCHAR, $3::NUMERIC(12, 6), $4::BOOLEAN)]
[parameters: [(9, 'ASELS', 1.539681, True), (9, 'FROTO', 1.257843, True), (9, 'TOASO', 1.191047, True)]]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
2026-06-27 23:11:16,146 - services.sector_benchmarks - ERROR - Failed to compute asset_turnover: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('asset_turnover', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:16,261 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('current_ratio', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:16,368 - services.sector_benchmarks - ERROR - Failed to compute debt_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('debt_ratio', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:16,947 - services.sector_benchmarks - ERROR - Failed to compute debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('debt_to_equity', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:17,054 - services.sector_benchmarks - ERROR - Failed to compute ebitda_margin: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('ebitda_margin', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:17,164 - services.sector_benchmarks - ERROR - Failed to compute gross_margin: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('gross_margin', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:17,749 - services.sector_benchmarks - ERROR - Failed to compute net_debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('net_debt_to_equity', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:17,856 - services.sector_benchmarks - ERROR - Failed to compute net_margin: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('net_margin', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:17,965 - services.sector_benchmarks - ERROR - Failed to compute receivables_turnover: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('receivables_turnover', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:18,075 - services.sector_benchmarks - ERROR - Failed to compute roa: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('roa', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:18,183 - services.sector_benchmarks - ERROR - Failed to compute roe: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('roe', 'Otomotiv & Savunma & Makine', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/12 ratios'
Arguments: ()
2026-06-27 23:11:18,183 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/12 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Otomotiv & Savunma & Makine 2026Q1: 0 benchmarks (3/6)'
Arguments: ()
2026-06-27 23:11:18,197 - __main__ - INFO - ✅ Otomotiv & Savunma & Makine 2026Q1: 0 benchmarks (3/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Sanayi & Metal & Kimya 2026Q1'
Arguments: ()
2026-06-27 23:11:18,309 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Sanayi & Meta l & Kimya 2026Q1
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for asset_turnover: n=0'
Arguments: ()
2026-06-27 23:11:18,966 - services.sector_benchmarks - INFO - 📊 Insufficient peers for asset_turnover: n=0
2026-06-27 23:11:18,972 - services.sector_benchmarks - ERROR - Failed to compute asset_turnover: cannot access local variable 'stmt' where it is not associated with a value
2026-06-27 23:11:19,409 - services.sector_benchmarks - ERROR - Failed to compute gross_margin: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "uq_benchmark_peers_id_ticker"
DETAIL:  Key (benchmark_id, ticker)=(15, EREGL) already exists.
[SQL: INSERT INTO sector_benchmark_peers (benchmark_id, ticker, ratio_value, is_included) VALUES ($1::INTEGER, $2::VARCHAR, $3::NUMERIC(12, 6), $4::BOOLEAN)]
[parameters: [(15, 'EREGL', -0.091736, True), (15, 'KRDMD', -0.075562, True), (15, 'AKCNS', -0.125816, True)]]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
2026-06-27 23:11:19,518 - services.sector_benchmarks - ERROR - Failed to compute debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('debt_to_equity', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:19,627 - services.sector_benchmarks - ERROR - Failed to compute receivables_turnover: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('receivables_turnover', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:19,735 - services.sector_benchmarks - ERROR - Failed to compute roa: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('roa', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:19,846 - services.sector_benchmarks - ERROR - Failed to compute net_margin: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('net_margin', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,090 - services.sector_benchmarks - ERROR - Failed to compute net_debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('net_debt_to_equity', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,200 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('current_ratio', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,444 - services.sector_benchmarks - ERROR - Failed to compute ebitda_margin: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('ebitda_margin', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,555 - services.sector_benchmarks - ERROR - Failed to compute roe: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('roe', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,801 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('acid_test_ratio', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:20,910 - services.sector_benchmarks - ERROR - Failed to compute debt_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('debt_ratio', 'Sanayi & Metal & Kimya', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/12 ratios'
Arguments: ()
2026-06-27 23:11:20,910 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/12 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Sanayi & Metal & Kimya 2026Q1: 0 benchmarks (4/6)'
Arguments: ()
2026-06-27 23:11:20,924 - __main__ - INFO - ✅ Sanayi & Metal & Kimya 2026Q1: 0 benchmarks (4/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Tüketim & Perakende & Tekstil 2026Q1'
Arguments: ()
2026-06-27 23:11:21,035 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Tüketim & Per akende & Tekstil 2026Q1
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for net_margin: n=1'
Arguments: ()
2026-06-27 23:11:21,684 - services.sector_benchmarks - INFO - 📊 Insufficient peers for net_margin: n=1
2026-06-27 23:11:21,690 - services.sector_benchmarks - ERROR - Failed to compute net_margin: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for ebitda_margin: n=1'
Arguments: ()
2026-06-27 23:11:21,797 - services.sector_benchmarks - INFO - 📊 Insufficient peers for ebitda_margin: n=1
2026-06-27 23:11:21,803 - services.sector_benchmarks - ERROR - Failed to compute ebitda_margin: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for debt_ratio: n=1'
Arguments: ()
2026-06-27 23:11:21,912 - services.sector_benchmarks - INFO - 📊 Insufficient peers for debt_ratio: n=1
2026-06-27 23:11:21,917 - services.sector_benchmarks - ERROR - Failed to compute debt_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for asset_turnover: n=0'
Arguments: ()
2026-06-27 23:11:22,025 - services.sector_benchmarks - INFO - 📊 Insufficient peers for asset_turnover: n=0
2026-06-27 23:11:22,036 - services.sector_benchmarks - ERROR - Failed to compute asset_turnover: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for gross_margin: n=1'
Arguments: ()
2026-06-27 23:11:22,146 - services.sector_benchmarks - INFO - 📊 Insufficient peers for gross_margin: n=1
2026-06-27 23:11:22,152 - services.sector_benchmarks - ERROR - Failed to compute gross_margin: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for debt_to_equity: n=1'
Arguments: ()
2026-06-27 23:11:22,259 - services.sector_benchmarks - INFO - 📊 Insufficient peers for debt_to_equity: n=1
2026-06-27 23:11:22,265 - services.sector_benchmarks - ERROR - Failed to compute debt_to_equity: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for receivables_turnover: n=0'
Arguments: ()
2026-06-27 23:11:22,374 - services.sector_benchmarks - INFO - 📊 Insufficient peers for receivables_turnover: n=0
2026-06-27 23:11:22,382 - services.sector_benchmarks - ERROR - Failed to compute receivables_turnover: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for roa: n=1'
Arguments: ()
2026-06-27 23:11:22,494 - services.sector_benchmarks - INFO - 📊 Insufficient peers for roa: n=1
2026-06-27 23:11:22,499 - services.sector_benchmarks - ERROR - Failed to compute roa: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for net_debt_to_equity: n=0'
Arguments: ()
2026-06-27 23:11:22,608 - services.sector_benchmarks - INFO - 📊 Insufficient peers for net_debt_to_equity: n=0
2026-06-27 23:11:22,615 - services.sector_benchmarks - ERROR - Failed to compute net_debt_to_equity: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for current_ratio: n=1'
Arguments: ()
2026-06-27 23:11:22,725 - services.sector_benchmarks - INFO - 📊 Insufficient peers for current_ratio: n=1
2026-06-27 23:11:22,733 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for roe: n=1'
Arguments: ()
2026-06-27 23:11:22,841 - services.sector_benchmarks - INFO - 📊 Insufficient peers for roe: n=1
2026-06-27 23:11:22,849 - services.sector_benchmarks - ERROR - Failed to compute roe: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 249, in compute_sector_benchmarks
    logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
Message: '📊 Insufficient peers for acid_test_ratio: n=1'
Arguments: ()
2026-06-27 23:11:22,957 - services.sector_benchmarks - INFO - 📊 Insufficient peers for acid_test_ratio: n=1
2026-06-27 23:11:22,964 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: cannot access local variable 'stmt' where it is not associated with a value
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/12 ratios'
Arguments: ()
2026-06-27 23:11:22,965 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/12 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Tüketim & Perakende & Tekstil 2026Q1: 0 benchmarks (5/6)'
Arguments: ()
2026-06-27 23:11:22,967 - __main__ - INFO - ✅ Tüketim & Perakende & Tekstil 2026Q1: 0 benchmarks (5/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9ee' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 226, in compute_sector_benchmarks
    logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
Message: '🧮 Computing benchmarks: Ulaştırma & Lojistik 2026Q1'
Arguments: ()
2026-06-27 23:11:23,078 - services.sector_benchmarks - INFO - 🧮 Computing benchmarks: Ulaştırma & L ojistik 2026Q1
2026-06-27 23:11:24,062 - services.sector_benchmarks - ERROR - Failed to compute acid_test_ratio: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "uq_benchmark_peers_id_ticker"
DETAIL:  Key (benchmark_id, ticker)=(1, PGSUS) already exists.
[SQL: INSERT INTO sector_benchmark_peers (benchmark_id, ticker, ratio_value, is_included) VALUES ($1::INTEGER, $2::VARCHAR, $3::NUMERIC(12, 6), $4::BOOLEAN)]
[parameters: [(1, 'PGSUS', 0.968575, True), (1, 'CLEBI', 1.260694, True), (1, 'THYAO', 0.974471, True)]]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
2026-06-27 23:11:24,309 - services.sector_benchmarks - ERROR - Failed to compute current_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('current_ratio', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,419 - services.sector_benchmarks - ERROR - Failed to compute debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('debt_to_equity', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,529 - services.sector_benchmarks - ERROR - Failed to compute net_debt_to_equity: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('net_debt_to_equity', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,638 - services.sector_benchmarks - ERROR - Failed to compute pb_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('pb_ratio', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,747 - services.sector_benchmarks - ERROR - Failed to compute pe_ratio: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('pe_ratio', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,856 - services.sector_benchmarks - ERROR - Failed to compute receivables_turnover: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('receivables_turnover', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-06-27 23:11:24,963 - services.sector_benchmarks - ERROR - Failed to compute roe: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InFailedSQLTransactionError'>: current transaction is aborted, commands ignored until end of transaction block
[SQL:
            SELECT
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*)
                    FROM company_ratios cr2
                    WHERE cr2.ticker = cr.ticker
                      AND cr2.ratio_code = $1
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = $2
              AND cr.ratio_code = $1
              AND cr.period_key = $3
              AND c.is_active = true
        ]
[parameters: ('roe', 'Ulaştırma & Lojistik', '2026Q1')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 62: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 341, in _phase_calculate_benchmarks
    benchmarks = await service.compute_sector_benchmarks(
  File "C:\Users\ASUS\hp\comp\services\sector_benchmarks.py", line 272, in compute_sector_benchmarks
    logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
Message: '✅ Benchmarks computed: 0/8 ratios'
Arguments: ()
2026-06-27 23:11:24,964 - services.sector_benchmarks - INFO - ✅ Benchmarks computed: 0/8 ratios
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 348, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Ulaştırma & Lojistik 2026Q1: 0 benchmarks (6/6)'
Arguments: ()
2026-06-27 23:11:24,982 - __main__ - INFO - ✅ Ulaştırma & Lojistik 2026Q1: 0 benchmarks (6/6)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 140, in run
    await self._phase_calculate_benchmarks()
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 358, in _phase_calculate_benchmarks
    logger.info(
Message: '✅ Benchmark calculation complete: 0 benchmarks, 0 failed'
Arguments: ()
2026-06-27 23:11:25,092 - __main__ - INFO - ✅ Benchmark calculation complete: 0 benchmarks, 0 failed
C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py:143: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  self.stats.end_time = datetime.utcnow()
2026-06-27 23:11:25,102 - __main__ - INFO -
2026-06-27 23:11:25,102 - __main__ - INFO - ============================================================
2026-06-27 23:11:25,103 - __main__ - INFO - BOOTSTRAP COMPLETE - FINAL REPORT
2026-06-27 23:11:25,103 - __main__ - INFO - ============================================================
2026-06-27 23:11:25,103 - __main__ - INFO - Duration: 11.3 minutes
2026-06-27 23:11:25,103 - __main__ - INFO -
2026-06-27 23:11:25,104 - __main__ - INFO - PHASE 1: MALI TABLO FETCH
2026-06-27 23:11:25,104 - __main__ - INFO -   Total companies: 57
2026-06-27 23:11:25,104 - __main__ - INFO -   Successful: 57
2026-06-27 23:11:25,104 - __main__ - INFO -   Failed: 0
2026-06-27 23:11:25,104 - __main__ - INFO -   Total rows inserted: 10,669
2026-06-27 23:11:25,104 - __main__ - INFO -
2026-06-27 23:11:25,105 - __main__ - INFO - PHASE 2: RATIO CALCULATION
2026-06-27 23:11:25,105 - __main__ - INFO -   Total ratios calculated: 0
2026-06-27 23:11:25,105 - __main__ - INFO -
2026-06-27 23:11:25,105 - __main__ - INFO - PHASE 3: SECTOR BENCHMARKS
2026-06-27 23:11:25,105 - __main__ - INFO -   Total benchmarks created: 0
2026-06-27 23:11:25,106 - __main__ - INFO -
2026-06-27 23:11:25,106 - __main__ - INFO - ============================================================
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1254.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 629, in <module>
    asyncio.run(main())
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 651, in run_until_complete
    self.run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 618, in run_forever
    self._run_once()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1951, in _run_once
    handle._run()
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 625, in main
    await engine.run(resume=args.resume)
  File "C:\Users\ASUS\hp\comp\bootstrap_comp_engine.py", line 152, in run
    logger.info("✅ Bootstrap completed successfully!")
Message: '✅ Bootstrap completed successfully!'
Arguments: ()
2026-06-27 23:11:25,106 - __main__ - INFO - ✅ Bootstrap completed successfully!

C:\Users\ASUS\hp\comp>