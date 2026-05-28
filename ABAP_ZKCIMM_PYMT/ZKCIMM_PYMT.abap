FUNCTION zkcimm_pymt.
*"----------------------------------------------------------------------
*"*"Local Interface:
*"  IMPORTING
*"     VALUE(IT_DATA) TYPE  ZTT_ZMMPEJABAT
*"  EXPORTING
*"     VALUE(EV_MESSAGE) TYPE  STRING
*"     VALUE(EV_STATUS) TYPE  CHAR1
*"----------------------------------------------------------------------

  IF it_data[] IS INITIAL.
    ev_status = 'E'.
    ev_message = 'Tidak ada data masuk atau dikirim'.
    RETURN.
  ENDIF.

  DATA: lt_copy_data TYPE ztt_zmmpejabat,
        lt_existing  TYPE STANDARD TABLE OF zmmpejabat.

  lt_copy_data = it_data.
  SELECT * FROM zmmpejabat INTO TABLE lt_existing
    FOR ALL ENTRIES IN lt_copy_data
    WHERE desk_kode_rel = lt_copy_data-desk_kode_rel.

  SORT lt_existing BY desk_kode_rel.

  LOOP AT lt_copy_data ASSIGNING FIELD-SYMBOL(<fs_data>).
    REPLACE ALL OCCURRENCES OF '-' IN <fs_data>-begda WITH ''.
    REPLACE ALL OCCURRENCES OF '-' IN <fs_data>-endda WITH ''.

    IF <fs_data>-endda IS INITIAL. "<-- kondisi PYMT tanggal mulai ada tapi tanggal berakhir tidak di set
      IF <fs_data>-begda IS NOT INITIAL.
        <fs_data>-endda = '99991231'.
      ELSE.
        <fs_data>-endda = ''.
      ENDIF.
    ENDIF.

    READ TABLE lt_existing ASSIGNING FIELD-SYMBOL(<fs_exist>)
      WITH KEY desk_kode_rel = <fs_data>-desk_kode_rel
      BINARY SEARCH.

    IF sy-subrc EQ 0.
      IF <fs_data>-id_pejabat IS INITIAL.
        <fs_data>-id_pejabat = <fs_exist>-id_pejabat.
      ENDIF.
      IF <fs_data>-tanda_tangan EQ 'NONE'.
        IF <fs_exist>-tanda_tangan IS NOT INITIAL.
          <fs_data>-tanda_tangan = <fs_exist>-tanda_tangan.
        ENDIF.
      ENDIF.

      IF <fs_exist>-endda LT sy-datum.
        IF <fs_data>-endda LT sy-datum OR <fs_data>-endda IS INITIAL. "<-- kondisi update jika pymt sudah selesai maka delete value
          <fs_data>-begda = '00000000'.
          <fs_data>-endda = '00000000'.
          <fs_data>-kode_pymt = ''.
        ENDIF.
      ENDIF.
    ENDIF.
  ENDLOOP.

  MODIFY zmmpejabat FROM TABLE lt_copy_data.

  IF sy-subrc EQ 0.
    COMMIT WORK AND WAIT.
    DATA: lv_lines TYPE i.
    DESCRIBE TABLE lt_copy_data LINES lv_lines.
    ev_status = 'S'.
    ev_message = |Data berhasil dan selesai di-sync, Total row: { lv_lines }|.
  ELSE.
    ROLLBACK WORK.
    ev_status = 'E'.
    ev_message = 'Gagal sync data, harap cek data yang dikirim'.
  ENDIF.

ENDFUNCTION.
