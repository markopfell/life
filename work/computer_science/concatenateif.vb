'https://www.extendoffice.com/documents/excel/2723-excel-concatenate-based-on-criteria.html
Function ConcatenateIf(CriteriaRange As Range, Condition As Variant, ConcatenateRange As Range, Optional Separator As String = ",") As Variant
'Update 20150414
Dim xResult As String
On Error Resume Next
If CriteriaRange.Count <> ConcatenateRange.Count Then
    ConcatenateIf = CVErr(xlErrRef)
    Exit Function
End If
For i = 1 To CriteriaRange.Count
    If CriteriaRange.Cells(i).Value = Condition Then
        xResult = xResult & Separator & ConcatenateRange.Cells(i).Value
    End If
Next i
If xResult <> "" Then
    xResult = VBA.Mid(xResult, VBA.Len(Separator) + 1)
End If
ConcatenateIf = xResult
Exit Function
End Function
