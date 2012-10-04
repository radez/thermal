<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h1>Events for <xsl:value-of select="DescribeStackEventsResponse/DescribeStackEventsResult/StackEvents/member/StackName"/></h1>
  <table border="0" width="800">
    <xsl:for-each select="DescribeStackEventsResponse/DescribeStackEventsResult/StackEvents/member">
    <tr>
      <td><xsl:value-of select="EventId"/></td>
      <td><xsl:value-of select="StackName"/></td>
      <td><xsl:value-of select="Timestamp"/></td>
      <td><xsl:value-of select="ResourceStatus"/></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
