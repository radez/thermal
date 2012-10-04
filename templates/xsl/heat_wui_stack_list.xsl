<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h1>Stacks</h1>
  <table border="0" width="800">
    <tr>
      <td colspan="2">---------------------------------------------------------------------------------------------------------</td>
    </tr>
    <xsl:for-each select="ListStacksResponse/ListStacksResult/StackSummaries/member">
    <tr>
      <td><b><xsl:value-of select="StackName"/></b></td>
      <td><a href="/event/list/{StackName}/">event list</a> ||
          <a href="/stack/delete/{StackName}/">delete stack</a></td>
    </tr>
    <tr>
      <td colspan="2"><xsl:value-of select="TemplateDescription"/></td>
    </tr>
    <tr>
      <td colspan="2">.</td>
    </tr>
    <tr>
      <td>Created: <xsl:value-of select="CreationTime"/></td>
      <td>Last Update: <xsl:value-of select="LastUpdatedTime"/></td>
    </tr>
    <tr>
      <td colspan="2">.</td>
    </tr>
    <tr>
      <td colspan="2">Status: <xsl:value-of select="StackStatusReason"/></td>
    </tr>
    <tr>
      <td colspan="2">---------------------------------------------------------------------------------------------------------</td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
