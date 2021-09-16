# Generated from SQLParser.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .SQLParser import SQLParser
else:
    from SQLParser import SQLParser

"""
Copyright (c) 2018, 2020, Oracle and/or its affiliates. All rights reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License, version 2.0,
as published by the Free Software Foundation.

This program is also distributed with certain software (including
but not limited to OpenSSL) that is licensed under separate terms, as
designated in a particular file or component or in included license
documentation. The authors of MySQL hereby grant you an additional
permission to link the program and your derivative works with the
separately licensed software that they have included with MySQL.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
the GNU General Public License, version 2.0, for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
"""
# mypy: ignore-errors
from jasmine.sql.parser.sql_base import *


# This class defines a complete generic visitor for a parse tree produced by SQLParser.


class SQLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SQLParser#sqlProgram.
    def visitSqlProgram(self, ctx: SQLParser.SqlProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#statement.
    def visitStatement(self, ctx: SQLParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleStatement.
    def visitSimpleStatement(self, ctx: SQLParser.SimpleStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterStatement.
    def visitAlterStatement(self, ctx: SQLParser.AlterStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterDatabase.
    def visitAlterDatabase(self, ctx: SQLParser.AlterDatabaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterEvent.
    def visitAlterEvent(self, ctx: SQLParser.AlterEventContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterLogfileGroup.
    def visitAlterLogfileGroup(self, ctx: SQLParser.AlterLogfileGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterLogfileGroupOptions.
    def visitAlterLogfileGroupOptions(
        self, ctx: SQLParser.AlterLogfileGroupOptionsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterLogfileGroupOption.
    def visitAlterLogfileGroupOption(
        self, ctx: SQLParser.AlterLogfileGroupOptionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterServer.
    def visitAlterServer(self, ctx: SQLParser.AlterServerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterTable.
    def visitAlterTable(self, ctx: SQLParser.AlterTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterTableActions.
    def visitAlterTableActions(self, ctx: SQLParser.AlterTableActionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterCommandList.
    def visitAlterCommandList(self, ctx: SQLParser.AlterCommandListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterCommandsModifierList.
    def visitAlterCommandsModifierList(
        self, ctx: SQLParser.AlterCommandsModifierListContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#standaloneAlterCommands.
    def visitStandaloneAlterCommands(
        self, ctx: SQLParser.StandaloneAlterCommandsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterPartition.
    def visitAlterPartition(self, ctx: SQLParser.AlterPartitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterList.
    def visitAlterList(self, ctx: SQLParser.AlterListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterCommandsModifier.
    def visitAlterCommandsModifier(self, ctx: SQLParser.AlterCommandsModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterListItem.
    def visitAlterListItem(self, ctx: SQLParser.AlterListItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#place.
    def visitPlace(self, ctx: SQLParser.PlaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#restrict.
    def visitRestrict(self, ctx: SQLParser.RestrictContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterOrderList.
    def visitAlterOrderList(self, ctx: SQLParser.AlterOrderListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterAlgorithmOption.
    def visitAlterAlgorithmOption(self, ctx: SQLParser.AlterAlgorithmOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterLockOption.
    def visitAlterLockOption(self, ctx: SQLParser.AlterLockOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexLockAndAlgorithm.
    def visitIndexLockAndAlgorithm(self, ctx: SQLParser.IndexLockAndAlgorithmContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#withValidation.
    def visitWithValidation(self, ctx: SQLParser.WithValidationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#removePartitioning.
    def visitRemovePartitioning(self, ctx: SQLParser.RemovePartitioningContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#allOrPartitionNameList.
    def visitAllOrPartitionNameList(self, ctx: SQLParser.AllOrPartitionNameListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterTablespace.
    def visitAlterTablespace(self, ctx: SQLParser.AlterTablespaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterUndoTablespace.
    def visitAlterUndoTablespace(self, ctx: SQLParser.AlterUndoTablespaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#undoTableSpaceOptions.
    def visitUndoTableSpaceOptions(self, ctx: SQLParser.UndoTableSpaceOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#undoTableSpaceOption.
    def visitUndoTableSpaceOption(self, ctx: SQLParser.UndoTableSpaceOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterTablespaceOptions.
    def visitAlterTablespaceOptions(self, ctx: SQLParser.AlterTablespaceOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterTablespaceOption.
    def visitAlterTablespaceOption(self, ctx: SQLParser.AlterTablespaceOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#changeTablespaceOption.
    def visitChangeTablespaceOption(self, ctx: SQLParser.ChangeTablespaceOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterView.
    def visitAlterView(self, ctx: SQLParser.AlterViewContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewTail.
    def visitViewTail(self, ctx: SQLParser.ViewTailContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewSelect.
    def visitViewSelect(self, ctx: SQLParser.ViewSelectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewCheckOption.
    def visitViewCheckOption(self, ctx: SQLParser.ViewCheckOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createStatement.
    def visitCreateStatement(self, ctx: SQLParser.CreateStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createDatabase.
    def visitCreateDatabase(self, ctx: SQLParser.CreateDatabaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createDatabaseOption.
    def visitCreateDatabaseOption(self, ctx: SQLParser.CreateDatabaseOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTable.
    def visitCreateTable(self, ctx: SQLParser.CreateTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableElementList.
    def visitTableElementList(self, ctx: SQLParser.TableElementListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableElement.
    def visitTableElement(self, ctx: SQLParser.TableElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#duplicateAsQueryExpression.
    def visitDuplicateAsQueryExpression(
        self, ctx: SQLParser.DuplicateAsQueryExpressionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#queryExpressionOrParens.
    def visitQueryExpressionOrParens(
        self, ctx: SQLParser.QueryExpressionOrParensContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createRoutine.
    def visitCreateRoutine(self, ctx: SQLParser.CreateRoutineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createProcedure.
    def visitCreateProcedure(self, ctx: SQLParser.CreateProcedureContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createFunction.
    def visitCreateFunction(self, ctx: SQLParser.CreateFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUdf.
    def visitCreateUdf(self, ctx: SQLParser.CreateUdfContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#routineCreateOption.
    def visitRoutineCreateOption(self, ctx: SQLParser.RoutineCreateOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#routineAlterOptions.
    def visitRoutineAlterOptions(self, ctx: SQLParser.RoutineAlterOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#routineOption.
    def visitRoutineOption(self, ctx: SQLParser.RoutineOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createIndex.
    def visitCreateIndex(self, ctx: SQLParser.CreateIndexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexNameAndType.
    def visitIndexNameAndType(self, ctx: SQLParser.IndexNameAndTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createIndexTarget.
    def visitCreateIndexTarget(self, ctx: SQLParser.CreateIndexTargetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createLogfileGroup.
    def visitCreateLogfileGroup(self, ctx: SQLParser.CreateLogfileGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#logfileGroupOptions.
    def visitLogfileGroupOptions(self, ctx: SQLParser.LogfileGroupOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#logfileGroupOption.
    def visitLogfileGroupOption(self, ctx: SQLParser.LogfileGroupOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createServer.
    def visitCreateServer(self, ctx: SQLParser.CreateServerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#serverOptions.
    def visitServerOptions(self, ctx: SQLParser.ServerOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#serverOption.
    def visitServerOption(self, ctx: SQLParser.ServerOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTablespace.
    def visitCreateTablespace(self, ctx: SQLParser.CreateTablespaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUndoTablespace.
    def visitCreateUndoTablespace(self, ctx: SQLParser.CreateUndoTablespaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsDataFileName.
    def visitTsDataFileName(self, ctx: SQLParser.TsDataFileNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsDataFile.
    def visitTsDataFile(self, ctx: SQLParser.TsDataFileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tablespaceOptions.
    def visitTablespaceOptions(self, ctx: SQLParser.TablespaceOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tablespaceOption.
    def visitTablespaceOption(self, ctx: SQLParser.TablespaceOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionInitialSize.
    def visitTsOptionInitialSize(self, ctx: SQLParser.TsOptionInitialSizeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionUndoRedoBufferSize.
    def visitTsOptionUndoRedoBufferSize(
        self, ctx: SQLParser.TsOptionUndoRedoBufferSizeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionAutoextendSize.
    def visitTsOptionAutoextendSize(self, ctx: SQLParser.TsOptionAutoextendSizeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionMaxSize.
    def visitTsOptionMaxSize(self, ctx: SQLParser.TsOptionMaxSizeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionExtentSize.
    def visitTsOptionExtentSize(self, ctx: SQLParser.TsOptionExtentSizeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionNodegroup.
    def visitTsOptionNodegroup(self, ctx: SQLParser.TsOptionNodegroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionEngine.
    def visitTsOptionEngine(self, ctx: SQLParser.TsOptionEngineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionWait.
    def visitTsOptionWait(self, ctx: SQLParser.TsOptionWaitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionComment.
    def visitTsOptionComment(self, ctx: SQLParser.TsOptionCommentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionFileblockSize.
    def visitTsOptionFileblockSize(self, ctx: SQLParser.TsOptionFileblockSizeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tsOptionEncryption.
    def visitTsOptionEncryption(self, ctx: SQLParser.TsOptionEncryptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createView.
    def visitCreateView(self, ctx: SQLParser.CreateViewContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewReplaceOrAlgorithm.
    def visitViewReplaceOrAlgorithm(self, ctx: SQLParser.ViewReplaceOrAlgorithmContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewAlgorithm.
    def visitViewAlgorithm(self, ctx: SQLParser.ViewAlgorithmContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewSuid.
    def visitViewSuid(self, ctx: SQLParser.ViewSuidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTrigger.
    def visitCreateTrigger(self, ctx: SQLParser.CreateTriggerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#triggerFollowsPrecedesClause.
    def visitTriggerFollowsPrecedesClause(
        self, ctx: SQLParser.TriggerFollowsPrecedesClauseContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createEvent.
    def visitCreateEvent(self, ctx: SQLParser.CreateEventContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createRole.
    def visitCreateRole(self, ctx: SQLParser.CreateRoleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createSpatialReference.
    def visitCreateSpatialReference(self, ctx: SQLParser.CreateSpatialReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#srsAttribute.
    def visitSrsAttribute(self, ctx: SQLParser.SrsAttributeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropStatement.
    def visitDropStatement(self, ctx: SQLParser.DropStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropDatabase.
    def visitDropDatabase(self, ctx: SQLParser.DropDatabaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropEvent.
    def visitDropEvent(self, ctx: SQLParser.DropEventContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropFunction.
    def visitDropFunction(self, ctx: SQLParser.DropFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropProcedure.
    def visitDropProcedure(self, ctx: SQLParser.DropProcedureContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropIndex.
    def visitDropIndex(self, ctx: SQLParser.DropIndexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropLogfileGroup.
    def visitDropLogfileGroup(self, ctx: SQLParser.DropLogfileGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropLogfileGroupOption.
    def visitDropLogfileGroupOption(self, ctx: SQLParser.DropLogfileGroupOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropServer.
    def visitDropServer(self, ctx: SQLParser.DropServerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropTable.
    def visitDropTable(self, ctx: SQLParser.DropTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropTableSpace.
    def visitDropTableSpace(self, ctx: SQLParser.DropTableSpaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropTrigger.
    def visitDropTrigger(self, ctx: SQLParser.DropTriggerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropView.
    def visitDropView(self, ctx: SQLParser.DropViewContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropRole.
    def visitDropRole(self, ctx: SQLParser.DropRoleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropSpatialReference.
    def visitDropSpatialReference(self, ctx: SQLParser.DropSpatialReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropUndoTablespace.
    def visitDropUndoTablespace(self, ctx: SQLParser.DropUndoTablespaceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#renameTableStatement.
    def visitRenameTableStatement(self, ctx: SQLParser.RenameTableStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#renamePair.
    def visitRenamePair(self, ctx: SQLParser.RenamePairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#truncateTableStatement.
    def visitTruncateTableStatement(self, ctx: SQLParser.TruncateTableStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#importStatement.
    def visitImportStatement(self, ctx: SQLParser.ImportStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#callStatement.
    def visitCallStatement(self, ctx: SQLParser.CallStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#deleteStatement.
    def visitDeleteStatement(self, ctx: SQLParser.DeleteStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDelete.
    def visitPartitionDelete(self, ctx: SQLParser.PartitionDeleteContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#deleteStatementOption.
    def visitDeleteStatementOption(self, ctx: SQLParser.DeleteStatementOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#doStatement.
    def visitDoStatement(self, ctx: SQLParser.DoStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#handlerStatement.
    def visitHandlerStatement(self, ctx: SQLParser.HandlerStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#handlerReadOrScan.
    def visitHandlerReadOrScan(self, ctx: SQLParser.HandlerReadOrScanContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertStatement.
    def visitInsertStatement(self, ctx: SQLParser.InsertStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertLockOption.
    def visitInsertLockOption(self, ctx: SQLParser.InsertLockOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertFromConstructor.
    def visitInsertFromConstructor(self, ctx: SQLParser.InsertFromConstructorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fields.
    def visitFields(self, ctx: SQLParser.FieldsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertValues.
    def visitInsertValues(self, ctx: SQLParser.InsertValuesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertQueryExpression.
    def visitInsertQueryExpression(self, ctx: SQLParser.InsertQueryExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#valueList.
    def visitValueList(self, ctx: SQLParser.ValueListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#values.
    def visitValues(self, ctx: SQLParser.ValuesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#valuesReference.
    def visitValuesReference(self, ctx: SQLParser.ValuesReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertUpdateList.
    def visitInsertUpdateList(self, ctx: SQLParser.InsertUpdateListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#loadStatement.
    def visitLoadStatement(self, ctx: SQLParser.LoadStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dataOrXml.
    def visitDataOrXml(self, ctx: SQLParser.DataOrXmlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#xmlRowsIdentifiedBy.
    def visitXmlRowsIdentifiedBy(self, ctx: SQLParser.XmlRowsIdentifiedByContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#loadDataFileTail.
    def visitLoadDataFileTail(self, ctx: SQLParser.LoadDataFileTailContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#loadDataFileTargetList.
    def visitLoadDataFileTargetList(self, ctx: SQLParser.LoadDataFileTargetListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldOrVariableList.
    def visitFieldOrVariableList(self, ctx: SQLParser.FieldOrVariableListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#replaceStatement.
    def visitReplaceStatement(self, ctx: SQLParser.ReplaceStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectStatement.
    def visitSelectStatement(self, ctx: SQLParser.SelectStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectStatementWithInto.
    def visitSelectStatementWithInto(
        self, ctx: SQLParser.SelectStatementWithIntoContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#queryExpression.
    def visitQueryExpression(self, ctx: SQLParser.QueryExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#queryExpressionBody.
    def visitQueryExpressionBody(self, ctx: SQLParser.QueryExpressionBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#queryExpressionParens.
    def visitQueryExpressionParens(self, ctx: SQLParser.QueryExpressionParensContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#queryPrimary.
    def visitQueryPrimary(self, ctx: SQLParser.QueryPrimaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#querySpecification.
    def visitQuerySpecification(self, ctx: SQLParser.QuerySpecificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#subquery.
    def visitSubquery(self, ctx: SQLParser.SubqueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#querySpecOption.
    def visitQuerySpecOption(self, ctx: SQLParser.QuerySpecOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#limitClause.
    def visitLimitClause(self, ctx: SQLParser.LimitClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleLimitClause.
    def visitSimpleLimitClause(self, ctx: SQLParser.SimpleLimitClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#limitOptions.
    def visitLimitOptions(self, ctx: SQLParser.LimitOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#limitOption.
    def visitLimitOption(self, ctx: SQLParser.LimitOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#intoClause.
    def visitIntoClause(self, ctx: SQLParser.IntoClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#procedureAnalyseClause.
    def visitProcedureAnalyseClause(self, ctx: SQLParser.ProcedureAnalyseClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#havingClause.
    def visitHavingClause(self, ctx: SQLParser.HavingClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowClause.
    def visitWindowClause(self, ctx: SQLParser.WindowClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowDefinition.
    def visitWindowDefinition(self, ctx: SQLParser.WindowDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowSpec.
    def visitWindowSpec(self, ctx: SQLParser.WindowSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowSpecDetails.
    def visitWindowSpecDetails(self, ctx: SQLParser.WindowSpecDetailsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameClause.
    def visitWindowFrameClause(self, ctx: SQLParser.WindowFrameClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameUnits.
    def visitWindowFrameUnits(self, ctx: SQLParser.WindowFrameUnitsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameExtent.
    def visitWindowFrameExtent(self, ctx: SQLParser.WindowFrameExtentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameStart.
    def visitWindowFrameStart(self, ctx: SQLParser.WindowFrameStartContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameBetween.
    def visitWindowFrameBetween(self, ctx: SQLParser.WindowFrameBetweenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameBound.
    def visitWindowFrameBound(self, ctx: SQLParser.WindowFrameBoundContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFrameExclusion.
    def visitWindowFrameExclusion(self, ctx: SQLParser.WindowFrameExclusionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#withClause.
    def visitWithClause(self, ctx: SQLParser.WithClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#commonTableExpression.
    def visitCommonTableExpression(self, ctx: SQLParser.CommonTableExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#groupByClause.
    def visitGroupByClause(self, ctx: SQLParser.GroupByClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#olapOption.
    def visitOlapOption(self, ctx: SQLParser.OlapOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#orderClause.
    def visitOrderClause(self, ctx: SQLParser.OrderClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#direction.
    def visitDirection(self, ctx: SQLParser.DirectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fromClause.
    def visitFromClause(self, ctx: SQLParser.FromClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableReferenceList.
    def visitTableReferenceList(self, ctx: SQLParser.TableReferenceListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableValueConstructor.
    def visitTableValueConstructor(self, ctx: SQLParser.TableValueConstructorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#explicitTable.
    def visitExplicitTable(self, ctx: SQLParser.ExplicitTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#rowValueExplicit.
    def visitRowValueExplicit(self, ctx: SQLParser.RowValueExplicitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectOption.
    def visitSelectOption(self, ctx: SQLParser.SelectOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockingClauseList.
    def visitLockingClauseList(self, ctx: SQLParser.LockingClauseListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockingClause.
    def visitLockingClause(self, ctx: SQLParser.LockingClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockStrengh.
    def visitLockStrengh(self, ctx: SQLParser.LockStrenghContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockedRowAction.
    def visitLockedRowAction(self, ctx: SQLParser.LockedRowActionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectItemList.
    def visitSelectItemList(self, ctx: SQLParser.SelectItemListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectItem.
    def visitSelectItem(self, ctx: SQLParser.SelectItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#selectAlias.
    def visitSelectAlias(self, ctx: SQLParser.SelectAliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#whereClause.
    def visitWhereClause(self, ctx: SQLParser.WhereClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableReference.
    def visitTableReference(self, ctx: SQLParser.TableReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#escapedTableReference.
    def visitEscapedTableReference(self, ctx: SQLParser.EscapedTableReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#joinedTable.
    def visitJoinedTable(self, ctx: SQLParser.JoinedTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#naturalJoinType.
    def visitNaturalJoinType(self, ctx: SQLParser.NaturalJoinTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#innerJoinType.
    def visitInnerJoinType(self, ctx: SQLParser.InnerJoinTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#outerJoinType.
    def visitOuterJoinType(self, ctx: SQLParser.OuterJoinTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableFactor.
    def visitTableFactor(self, ctx: SQLParser.TableFactorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#singleTable.
    def visitSingleTable(self, ctx: SQLParser.SingleTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#singleTableParens.
    def visitSingleTableParens(self, ctx: SQLParser.SingleTableParensContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#derivedTable.
    def visitDerivedTable(self, ctx: SQLParser.DerivedTableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableReferenceListParens.
    def visitTableReferenceListParens(
        self, ctx: SQLParser.TableReferenceListParensContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableFunction.
    def visitTableFunction(self, ctx: SQLParser.TableFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnsClause.
    def visitColumnsClause(self, ctx: SQLParser.ColumnsClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#jtColumn.
    def visitJtColumn(self, ctx: SQLParser.JtColumnContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#onEmptyOrError.
    def visitOnEmptyOrError(self, ctx: SQLParser.OnEmptyOrErrorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#onEmpty.
    def visitOnEmpty(self, ctx: SQLParser.OnEmptyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#onError.
    def visitOnError(self, ctx: SQLParser.OnErrorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#jtOnResponse.
    def visitJtOnResponse(self, ctx: SQLParser.JtOnResponseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#unionOption.
    def visitUnionOption(self, ctx: SQLParser.UnionOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableAlias.
    def visitTableAlias(self, ctx: SQLParser.TableAliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexHintList.
    def visitIndexHintList(self, ctx: SQLParser.IndexHintListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexHint.
    def visitIndexHint(self, ctx: SQLParser.IndexHintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexHintType.
    def visitIndexHintType(self, ctx: SQLParser.IndexHintTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyOrIndex.
    def visitKeyOrIndex(self, ctx: SQLParser.KeyOrIndexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#constraintKeyType.
    def visitConstraintKeyType(self, ctx: SQLParser.ConstraintKeyTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexHintClause.
    def visitIndexHintClause(self, ctx: SQLParser.IndexHintClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexList.
    def visitIndexList(self, ctx: SQLParser.IndexListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexListElement.
    def visitIndexListElement(self, ctx: SQLParser.IndexListElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#updateStatement.
    def visitUpdateStatement(self, ctx: SQLParser.UpdateStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#transactionOrLockingStatement.
    def visitTransactionOrLockingStatement(
        self, ctx: SQLParser.TransactionOrLockingStatementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#transactionStatement.
    def visitTransactionStatement(self, ctx: SQLParser.TransactionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#beginWork.
    def visitBeginWork(self, ctx: SQLParser.BeginWorkContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#transactionCharacteristic.
    def visitTransactionCharacteristic(
        self, ctx: SQLParser.TransactionCharacteristicContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#savepointStatement.
    def visitSavepointStatement(self, ctx: SQLParser.SavepointStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockStatement.
    def visitLockStatement(self, ctx: SQLParser.LockStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockItem.
    def visitLockItem(self, ctx: SQLParser.LockItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lockOption.
    def visitLockOption(self, ctx: SQLParser.LockOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#xaStatement.
    def visitXaStatement(self, ctx: SQLParser.XaStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#xaConvert.
    def visitXaConvert(self, ctx: SQLParser.XaConvertContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#xid.
    def visitXid(self, ctx: SQLParser.XidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#replicationStatement.
    def visitReplicationStatement(self, ctx: SQLParser.ReplicationStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resetOption.
    def visitResetOption(self, ctx: SQLParser.ResetOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#masterResetOptions.
    def visitMasterResetOptions(self, ctx: SQLParser.MasterResetOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#replicationLoad.
    def visitReplicationLoad(self, ctx: SQLParser.ReplicationLoadContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#changeMaster.
    def visitChangeMaster(self, ctx: SQLParser.ChangeMasterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#changeMasterOptions.
    def visitChangeMasterOptions(self, ctx: SQLParser.ChangeMasterOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#masterOption.
    def visitMasterOption(self, ctx: SQLParser.MasterOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#privilegeCheckDef.
    def visitPrivilegeCheckDef(self, ctx: SQLParser.PrivilegeCheckDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tablePrimaryKeyCheckDef.
    def visitTablePrimaryKeyCheckDef(
        self, ctx: SQLParser.TablePrimaryKeyCheckDefContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#masterTlsCiphersuitesDef.
    def visitMasterTlsCiphersuitesDef(
        self, ctx: SQLParser.MasterTlsCiphersuitesDefContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#masterFileDef.
    def visitMasterFileDef(self, ctx: SQLParser.MasterFileDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#serverIdList.
    def visitServerIdList(self, ctx: SQLParser.ServerIdListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#changeReplication.
    def visitChangeReplication(self, ctx: SQLParser.ChangeReplicationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterDefinition.
    def visitFilterDefinition(self, ctx: SQLParser.FilterDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterDbList.
    def visitFilterDbList(self, ctx: SQLParser.FilterDbListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterTableList.
    def visitFilterTableList(self, ctx: SQLParser.FilterTableListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterStringList.
    def visitFilterStringList(self, ctx: SQLParser.FilterStringListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterWildDbTableString.
    def visitFilterWildDbTableString(
        self, ctx: SQLParser.FilterWildDbTableStringContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterDbPairList.
    def visitFilterDbPairList(self, ctx: SQLParser.FilterDbPairListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#slave.
    def visitSlave(self, ctx: SQLParser.SlaveContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#slaveUntilOptions.
    def visitSlaveUntilOptions(self, ctx: SQLParser.SlaveUntilOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#slaveConnectionOptions.
    def visitSlaveConnectionOptions(self, ctx: SQLParser.SlaveConnectionOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#slaveThreadOptions.
    def visitSlaveThreadOptions(self, ctx: SQLParser.SlaveThreadOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#slaveThreadOption.
    def visitSlaveThreadOption(self, ctx: SQLParser.SlaveThreadOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#groupReplication.
    def visitGroupReplication(self, ctx: SQLParser.GroupReplicationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#preparedStatement.
    def visitPreparedStatement(self, ctx: SQLParser.PreparedStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#executeStatement.
    def visitExecuteStatement(self, ctx: SQLParser.ExecuteStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#executeVarList.
    def visitExecuteVarList(self, ctx: SQLParser.ExecuteVarListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cloneStatement.
    def visitCloneStatement(self, ctx: SQLParser.CloneStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dataDirSSL.
    def visitDataDirSSL(self, ctx: SQLParser.DataDirSSLContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ssl.
    def visitSsl(self, ctx: SQLParser.SslContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#accountManagementStatement.
    def visitAccountManagementStatement(
        self, ctx: SQLParser.AccountManagementStatementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterUser.
    def visitAlterUser(self, ctx: SQLParser.AlterUserContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterUserTail.
    def visitAlterUserTail(self, ctx: SQLParser.AlterUserTailContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#userFunction.
    def visitUserFunction(self, ctx: SQLParser.UserFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUser.
    def visitCreateUser(self, ctx: SQLParser.CreateUserContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUserTail.
    def visitCreateUserTail(self, ctx: SQLParser.CreateUserTailContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#defaultRoleClause.
    def visitDefaultRoleClause(self, ctx: SQLParser.DefaultRoleClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#requireClause.
    def visitRequireClause(self, ctx: SQLParser.RequireClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#connectOptions.
    def visitConnectOptions(self, ctx: SQLParser.ConnectOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#accountLockPasswordExpireOptions.
    def visitAccountLockPasswordExpireOptions(
        self, ctx: SQLParser.AccountLockPasswordExpireOptionsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropUser.
    def visitDropUser(self, ctx: SQLParser.DropUserContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grant.
    def visitGrant(self, ctx: SQLParser.GrantContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grantTargetList.
    def visitGrantTargetList(self, ctx: SQLParser.GrantTargetListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grantOptions.
    def visitGrantOptions(self, ctx: SQLParser.GrantOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exceptRoleList.
    def visitExceptRoleList(self, ctx: SQLParser.ExceptRoleListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#withRoles.
    def visitWithRoles(self, ctx: SQLParser.WithRolesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grantAs.
    def visitGrantAs(self, ctx: SQLParser.GrantAsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#versionedRequireClause.
    def visitVersionedRequireClause(self, ctx: SQLParser.VersionedRequireClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#renameUser.
    def visitRenameUser(self, ctx: SQLParser.RenameUserContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#revoke.
    def visitRevoke(self, ctx: SQLParser.RevokeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#onTypeTo.
    def visitOnTypeTo(self, ctx: SQLParser.OnTypeToContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#aclType.
    def visitAclType(self, ctx: SQLParser.AclTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleOrPrivilegesList.
    def visitRoleOrPrivilegesList(self, ctx: SQLParser.RoleOrPrivilegesListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleOrPrivilege.
    def visitRoleOrPrivilege(self, ctx: SQLParser.RoleOrPrivilegeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grantIdentifier.
    def visitGrantIdentifier(self, ctx: SQLParser.GrantIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#requireList.
    def visitRequireList(self, ctx: SQLParser.RequireListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#requireListElement.
    def visitRequireListElement(self, ctx: SQLParser.RequireListElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#grantOption.
    def visitGrantOption(self, ctx: SQLParser.GrantOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setRole.
    def visitSetRole(self, ctx: SQLParser.SetRoleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleList.
    def visitRoleList(self, ctx: SQLParser.RoleListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#role.
    def visitRole(self, ctx: SQLParser.RoleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableAdministrationStatement.
    def visitTableAdministrationStatement(
        self, ctx: SQLParser.TableAdministrationStatementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#histogram.
    def visitHistogram(self, ctx: SQLParser.HistogramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#checkOption.
    def visitCheckOption(self, ctx: SQLParser.CheckOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#repairType.
    def visitRepairType(self, ctx: SQLParser.RepairTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#installUninstallStatment.
    def visitInstallUninstallStatment(
        self, ctx: SQLParser.InstallUninstallStatmentContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setStatement.
    def visitSetStatement(self, ctx: SQLParser.SetStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#startOptionValueList.
    def visitStartOptionValueList(self, ctx: SQLParser.StartOptionValueListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#transactionCharacteristics.
    def visitTransactionCharacteristics(
        self, ctx: SQLParser.TransactionCharacteristicsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#transactionAccessMode.
    def visitTransactionAccessMode(self, ctx: SQLParser.TransactionAccessModeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#isolationLevel.
    def visitIsolationLevel(self, ctx: SQLParser.IsolationLevelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#optionValueListContinued.
    def visitOptionValueListContinued(
        self, ctx: SQLParser.OptionValueListContinuedContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#optionValueNoOptionType.
    def visitOptionValueNoOptionType(
        self, ctx: SQLParser.OptionValueNoOptionTypeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#optionValue.
    def visitOptionValue(self, ctx: SQLParser.OptionValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setSystemVariable.
    def visitSetSystemVariable(self, ctx: SQLParser.SetSystemVariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#startOptionValueListFollowingOptionType.
    def visitStartOptionValueListFollowingOptionType(
        self, ctx: SQLParser.StartOptionValueListFollowingOptionTypeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#optionValueFollowingOptionType.
    def visitOptionValueFollowingOptionType(
        self, ctx: SQLParser.OptionValueFollowingOptionTypeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setExprOrDefault.
    def visitSetExprOrDefault(self, ctx: SQLParser.SetExprOrDefaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#showStatement.
    def visitShowStatement(self, ctx: SQLParser.ShowStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#showCommandType.
    def visitShowCommandType(self, ctx: SQLParser.ShowCommandTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#nonBlocking.
    def visitNonBlocking(self, ctx: SQLParser.NonBlockingContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fromOrIn.
    def visitFromOrIn(self, ctx: SQLParser.FromOrInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#inDb.
    def visitInDb(self, ctx: SQLParser.InDbContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#profileType.
    def visitProfileType(self, ctx: SQLParser.ProfileTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#otherAdministrativeStatement.
    def visitOtherAdministrativeStatement(
        self, ctx: SQLParser.OtherAdministrativeStatementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyCacheListOrParts.
    def visitKeyCacheListOrParts(self, ctx: SQLParser.KeyCacheListOrPartsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyCacheList.
    def visitKeyCacheList(self, ctx: SQLParser.KeyCacheListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#assignToKeycache.
    def visitAssignToKeycache(self, ctx: SQLParser.AssignToKeycacheContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#assignToKeycachePartition.
    def visitAssignToKeycachePartition(
        self, ctx: SQLParser.AssignToKeycachePartitionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cacheKeyList.
    def visitCacheKeyList(self, ctx: SQLParser.CacheKeyListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyUsageElement.
    def visitKeyUsageElement(self, ctx: SQLParser.KeyUsageElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyUsageList.
    def visitKeyUsageList(self, ctx: SQLParser.KeyUsageListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#flushOption.
    def visitFlushOption(self, ctx: SQLParser.FlushOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#logType.
    def visitLogType(self, ctx: SQLParser.LogTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#flushTables.
    def visitFlushTables(self, ctx: SQLParser.FlushTablesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#flushTablesOptions.
    def visitFlushTablesOptions(self, ctx: SQLParser.FlushTablesOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#preloadTail.
    def visitPreloadTail(self, ctx: SQLParser.PreloadTailContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#preloadList.
    def visitPreloadList(self, ctx: SQLParser.PreloadListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#preloadKeys.
    def visitPreloadKeys(self, ctx: SQLParser.PreloadKeysContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#adminPartition.
    def visitAdminPartition(self, ctx: SQLParser.AdminPartitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resourceGroupManagement.
    def visitResourceGroupManagement(
        self, ctx: SQLParser.ResourceGroupManagementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createResourceGroup.
    def visitCreateResourceGroup(self, ctx: SQLParser.CreateResourceGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resourceGroupVcpuList.
    def visitResourceGroupVcpuList(self, ctx: SQLParser.ResourceGroupVcpuListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#vcpuNumOrRange.
    def visitVcpuNumOrRange(self, ctx: SQLParser.VcpuNumOrRangeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resourceGroupPriority.
    def visitResourceGroupPriority(self, ctx: SQLParser.ResourceGroupPriorityContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resourceGroupEnableDisable.
    def visitResourceGroupEnableDisable(
        self, ctx: SQLParser.ResourceGroupEnableDisableContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterResourceGroup.
    def visitAlterResourceGroup(self, ctx: SQLParser.AlterResourceGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setResourceGroup.
    def visitSetResourceGroup(self, ctx: SQLParser.SetResourceGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#threadIdList.
    def visitThreadIdList(self, ctx: SQLParser.ThreadIdListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dropResourceGroup.
    def visitDropResourceGroup(self, ctx: SQLParser.DropResourceGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#utilityStatement.
    def visitUtilityStatement(self, ctx: SQLParser.UtilityStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#describeStatement.
    def visitDescribeStatement(self, ctx: SQLParser.DescribeStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#explainStatement.
    def visitExplainStatement(self, ctx: SQLParser.ExplainStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#explainableStatement.
    def visitExplainableStatement(self, ctx: SQLParser.ExplainableStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#helpCommand.
    def visitHelpCommand(self, ctx: SQLParser.HelpCommandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#useCommand.
    def visitUseCommand(self, ctx: SQLParser.UseCommandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#restartServer.
    def visitRestartServer(self, ctx: SQLParser.RestartServerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprOr.
    def visitExprOr(self, ctx: SQLParser.ExprOrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprNot.
    def visitExprNot(self, ctx: SQLParser.ExprNotContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprIs.
    def visitExprIs(self, ctx: SQLParser.ExprIsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprAnd.
    def visitExprAnd(self, ctx: SQLParser.ExprAndContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprXor.
    def visitExprXor(self, ctx: SQLParser.ExprXorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#primaryExprPredicate.
    def visitPrimaryExprPredicate(self, ctx: SQLParser.PrimaryExprPredicateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#primaryExprCompare.
    def visitPrimaryExprCompare(self, ctx: SQLParser.PrimaryExprCompareContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#primaryExprAllAny.
    def visitPrimaryExprAllAny(self, ctx: SQLParser.PrimaryExprAllAnyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#primaryExprIsNull.
    def visitPrimaryExprIsNull(self, ctx: SQLParser.PrimaryExprIsNullContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#compOp.
    def visitCompOp(self, ctx: SQLParser.CompOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#predicate.
    def visitPredicate(self, ctx: SQLParser.PredicateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#predicateExprIn.
    def visitPredicateExprIn(self, ctx: SQLParser.PredicateExprInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#predicateExprBetween.
    def visitPredicateExprBetween(self, ctx: SQLParser.PredicateExprBetweenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#predicateExprLike.
    def visitPredicateExprLike(self, ctx: SQLParser.PredicateExprLikeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#predicateExprRegex.
    def visitPredicateExprRegex(self, ctx: SQLParser.PredicateExprRegexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#bitExpr.
    def visitBitExpr(self, ctx: SQLParser.BitExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprConvert.
    def visitSimpleExprConvert(self, ctx: SQLParser.SimpleExprConvertContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprVariable.
    def visitSimpleExprVariable(self, ctx: SQLParser.SimpleExprVariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprCast.
    def visitSimpleExprCast(self, ctx: SQLParser.SimpleExprCastContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprUnary.
    def visitSimpleExprUnary(self, ctx: SQLParser.SimpleExprUnaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprOdbc.
    def visitSimpleExprOdbc(self, ctx: SQLParser.SimpleExprOdbcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprRuntimeFunction.
    def visitSimpleExprRuntimeFunction(
        self, ctx: SQLParser.SimpleExprRuntimeFunctionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprFunction.
    def visitSimpleExprFunction(self, ctx: SQLParser.SimpleExprFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprCollate.
    def visitSimpleExprCollate(self, ctx: SQLParser.SimpleExprCollateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprMatch.
    def visitSimpleExprMatch(self, ctx: SQLParser.SimpleExprMatchContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprWindowingFunction.
    def visitSimpleExprWindowingFunction(
        self, ctx: SQLParser.SimpleExprWindowingFunctionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprBinary.
    def visitSimpleExprBinary(self, ctx: SQLParser.SimpleExprBinaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprColumnRef.
    def visitSimpleExprColumnRef(self, ctx: SQLParser.SimpleExprColumnRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprParamMarker.
    def visitSimpleExprParamMarker(self, ctx: SQLParser.SimpleExprParamMarkerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprSum.
    def visitSimpleExprSum(self, ctx: SQLParser.SimpleExprSumContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprConvertUsing.
    def visitSimpleExprConvertUsing(self, ctx: SQLParser.SimpleExprConvertUsingContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprSubQuery.
    def visitSimpleExprSubQuery(self, ctx: SQLParser.SimpleExprSubQueryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprGroupingOperation.
    def visitSimpleExprGroupingOperation(
        self, ctx: SQLParser.SimpleExprGroupingOperationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprNot.
    def visitSimpleExprNot(self, ctx: SQLParser.SimpleExprNotContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprValues.
    def visitSimpleExprValues(self, ctx: SQLParser.SimpleExprValuesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprDefault.
    def visitSimpleExprDefault(self, ctx: SQLParser.SimpleExprDefaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprList.
    def visitSimpleExprList(self, ctx: SQLParser.SimpleExprListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprInterval.
    def visitSimpleExprInterval(self, ctx: SQLParser.SimpleExprIntervalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprCase.
    def visitSimpleExprCase(self, ctx: SQLParser.SimpleExprCaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprConcat.
    def visitSimpleExprConcat(self, ctx: SQLParser.SimpleExprConcatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprLiteral.
    def visitSimpleExprLiteral(self, ctx: SQLParser.SimpleExprLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#arrayCast.
    def visitArrayCast(self, ctx: SQLParser.ArrayCastContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#jsonOperator.
    def visitJsonOperator(self, ctx: SQLParser.JsonOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#sumExpr.
    def visitSumExpr(self, ctx: SQLParser.SumExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#groupingOperation.
    def visitGroupingOperation(self, ctx: SQLParser.GroupingOperationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowFunctionCall.
    def visitWindowFunctionCall(self, ctx: SQLParser.WindowFunctionCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowingClause.
    def visitWindowingClause(self, ctx: SQLParser.WindowingClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#leadLagInfo.
    def visitLeadLagInfo(self, ctx: SQLParser.LeadLagInfoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#nullTreatment.
    def visitNullTreatment(self, ctx: SQLParser.NullTreatmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#jsonFunction.
    def visitJsonFunction(self, ctx: SQLParser.JsonFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#inSumExpr.
    def visitInSumExpr(self, ctx: SQLParser.InSumExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identListArg.
    def visitIdentListArg(self, ctx: SQLParser.IdentListArgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identList.
    def visitIdentList(self, ctx: SQLParser.IdentListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fulltextOptions.
    def visitFulltextOptions(self, ctx: SQLParser.FulltextOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#runtimeFunctionCall.
    def visitRuntimeFunctionCall(self, ctx: SQLParser.RuntimeFunctionCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#geometryFunction.
    def visitGeometryFunction(self, ctx: SQLParser.GeometryFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#timeFunctionParameters.
    def visitTimeFunctionParameters(self, ctx: SQLParser.TimeFunctionParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fractionalPrecision.
    def visitFractionalPrecision(self, ctx: SQLParser.FractionalPrecisionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#weightStringLevels.
    def visitWeightStringLevels(self, ctx: SQLParser.WeightStringLevelsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#weightStringLevelListItem.
    def visitWeightStringLevelListItem(
        self, ctx: SQLParser.WeightStringLevelListItemContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dateTimeTtype.
    def visitDateTimeTtype(self, ctx: SQLParser.DateTimeTtypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#trimFunction.
    def visitTrimFunction(self, ctx: SQLParser.TrimFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#substringFunction.
    def visitSubstringFunction(self, ctx: SQLParser.SubstringFunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#functionCall.
    def visitFunctionCall(self, ctx: SQLParser.FunctionCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#udfExprList.
    def visitUdfExprList(self, ctx: SQLParser.UdfExprListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#udfExpr.
    def visitUdfExpr(self, ctx: SQLParser.UdfExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#variable.
    def visitVariable(self, ctx: SQLParser.VariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#userVariable.
    def visitUserVariable(self, ctx: SQLParser.UserVariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#systemVariable.
    def visitSystemVariable(self, ctx: SQLParser.SystemVariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#internalVariableName.
    def visitInternalVariableName(self, ctx: SQLParser.InternalVariableNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#whenExpression.
    def visitWhenExpression(self, ctx: SQLParser.WhenExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#thenExpression.
    def visitThenExpression(self, ctx: SQLParser.ThenExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#elseExpression.
    def visitElseExpression(self, ctx: SQLParser.ElseExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#castType.
    def visitCastType(self, ctx: SQLParser.CastTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprList.
    def visitExprList(self, ctx: SQLParser.ExprListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#charset.
    def visitCharset(self, ctx: SQLParser.CharsetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#notRule.
    def visitNotRule(self, ctx: SQLParser.NotRuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#not2Rule.
    def visitNot2Rule(self, ctx: SQLParser.Not2RuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#interval.
    def visitInterval(self, ctx: SQLParser.IntervalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#intervalTimeStamp.
    def visitIntervalTimeStamp(self, ctx: SQLParser.IntervalTimeStampContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprListWithParentheses.
    def visitExprListWithParentheses(
        self, ctx: SQLParser.ExprListWithParenthesesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#exprWithParentheses.
    def visitExprWithParentheses(self, ctx: SQLParser.ExprWithParenthesesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleExprWithParentheses.
    def visitSimpleExprWithParentheses(
        self, ctx: SQLParser.SimpleExprWithParenthesesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#orderList.
    def visitOrderList(self, ctx: SQLParser.OrderListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#orderExpression.
    def visitOrderExpression(self, ctx: SQLParser.OrderExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#groupList.
    def visitGroupList(self, ctx: SQLParser.GroupListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#groupingExpression.
    def visitGroupingExpression(self, ctx: SQLParser.GroupingExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#channel.
    def visitChannel(self, ctx: SQLParser.ChannelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#compoundStatement.
    def visitCompoundStatement(self, ctx: SQLParser.CompoundStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#returnStatement.
    def visitReturnStatement(self, ctx: SQLParser.ReturnStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ifStatement.
    def visitIfStatement(self, ctx: SQLParser.IfStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ifBody.
    def visitIfBody(self, ctx: SQLParser.IfBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#thenStatement.
    def visitThenStatement(self, ctx: SQLParser.ThenStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#compoundStatementList.
    def visitCompoundStatementList(self, ctx: SQLParser.CompoundStatementListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#caseStatement.
    def visitCaseStatement(self, ctx: SQLParser.CaseStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#elseStatement.
    def visitElseStatement(self, ctx: SQLParser.ElseStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#labeledBlock.
    def visitLabeledBlock(self, ctx: SQLParser.LabeledBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#unlabeledBlock.
    def visitUnlabeledBlock(self, ctx: SQLParser.UnlabeledBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#label.
    def visitLabel(self, ctx: SQLParser.LabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#beginEndBlock.
    def visitBeginEndBlock(self, ctx: SQLParser.BeginEndBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#labeledControl.
    def visitLabeledControl(self, ctx: SQLParser.LabeledControlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#unlabeledControl.
    def visitUnlabeledControl(self, ctx: SQLParser.UnlabeledControlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#loopBlock.
    def visitLoopBlock(self, ctx: SQLParser.LoopBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#whileDoBlock.
    def visitWhileDoBlock(self, ctx: SQLParser.WhileDoBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#repeatUntilBlock.
    def visitRepeatUntilBlock(self, ctx: SQLParser.RepeatUntilBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#spDeclarations.
    def visitSpDeclarations(self, ctx: SQLParser.SpDeclarationsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#spDeclaration.
    def visitSpDeclaration(self, ctx: SQLParser.SpDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx: SQLParser.VariableDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#conditionDeclaration.
    def visitConditionDeclaration(self, ctx: SQLParser.ConditionDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#spCondition.
    def visitSpCondition(self, ctx: SQLParser.SpConditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#sqlstate.
    def visitSqlstate(self, ctx: SQLParser.SqlstateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#handlerDeclaration.
    def visitHandlerDeclaration(self, ctx: SQLParser.HandlerDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#handlerCondition.
    def visitHandlerCondition(self, ctx: SQLParser.HandlerConditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cursorDeclaration.
    def visitCursorDeclaration(self, ctx: SQLParser.CursorDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#iterateStatement.
    def visitIterateStatement(self, ctx: SQLParser.IterateStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#leaveStatement.
    def visitLeaveStatement(self, ctx: SQLParser.LeaveStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#getDiagnostics.
    def visitGetDiagnostics(self, ctx: SQLParser.GetDiagnosticsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#signalAllowedExpr.
    def visitSignalAllowedExpr(self, ctx: SQLParser.SignalAllowedExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#statementInformationItem.
    def visitStatementInformationItem(
        self, ctx: SQLParser.StatementInformationItemContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#conditionInformationItem.
    def visitConditionInformationItem(
        self, ctx: SQLParser.ConditionInformationItemContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#signalInformationItemName.
    def visitSignalInformationItemName(
        self, ctx: SQLParser.SignalInformationItemNameContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#signalStatement.
    def visitSignalStatement(self, ctx: SQLParser.SignalStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resignalStatement.
    def visitResignalStatement(self, ctx: SQLParser.ResignalStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#signalInformationItem.
    def visitSignalInformationItem(self, ctx: SQLParser.SignalInformationItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cursorOpen.
    def visitCursorOpen(self, ctx: SQLParser.CursorOpenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cursorClose.
    def visitCursorClose(self, ctx: SQLParser.CursorCloseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#cursorFetch.
    def visitCursorFetch(self, ctx: SQLParser.CursorFetchContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#schedule.
    def visitSchedule(self, ctx: SQLParser.ScheduleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnDefinition.
    def visitColumnDefinition(self, ctx: SQLParser.ColumnDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#checkOrReferences.
    def visitCheckOrReferences(self, ctx: SQLParser.CheckOrReferencesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#checkConstraint.
    def visitCheckConstraint(self, ctx: SQLParser.CheckConstraintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#constraintEnforcement.
    def visitConstraintEnforcement(self, ctx: SQLParser.ConstraintEnforcementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableConstraintDef.
    def visitTableConstraintDef(self, ctx: SQLParser.TableConstraintDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#constraintName.
    def visitConstraintName(self, ctx: SQLParser.ConstraintNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldDefinition.
    def visitFieldDefinition(self, ctx: SQLParser.FieldDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnAttribute.
    def visitColumnAttribute(self, ctx: SQLParser.ColumnAttributeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnFormat.
    def visitColumnFormat(self, ctx: SQLParser.ColumnFormatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#storageMedia.
    def visitStorageMedia(self, ctx: SQLParser.StorageMediaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#gcolAttribute.
    def visitGcolAttribute(self, ctx: SQLParser.GcolAttributeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#references.
    def visitReferences(self, ctx: SQLParser.ReferencesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#deleteOption.
    def visitDeleteOption(self, ctx: SQLParser.DeleteOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyList.
    def visitKeyList(self, ctx: SQLParser.KeyListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyPart.
    def visitKeyPart(self, ctx: SQLParser.KeyPartContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyListWithExpression.
    def visitKeyListWithExpression(self, ctx: SQLParser.KeyListWithExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyPartOrExpression.
    def visitKeyPartOrExpression(self, ctx: SQLParser.KeyPartOrExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#keyListVariants.
    def visitKeyListVariants(self, ctx: SQLParser.KeyListVariantsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexType.
    def visitIndexType(self, ctx: SQLParser.IndexTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexOption.
    def visitIndexOption(self, ctx: SQLParser.IndexOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#commonIndexOption.
    def visitCommonIndexOption(self, ctx: SQLParser.CommonIndexOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#visibility.
    def visitVisibility(self, ctx: SQLParser.VisibilityContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexTypeClause.
    def visitIndexTypeClause(self, ctx: SQLParser.IndexTypeClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fulltextIndexOption.
    def visitFulltextIndexOption(self, ctx: SQLParser.FulltextIndexOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#spatialIndexOption.
    def visitSpatialIndexOption(self, ctx: SQLParser.SpatialIndexOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dataTypeDefinition.
    def visitDataTypeDefinition(self, ctx: SQLParser.DataTypeDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dataType.
    def visitDataType(self, ctx: SQLParser.DataTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#nchar.
    def visitNchar(self, ctx: SQLParser.NcharContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#realType.
    def visitRealType(self, ctx: SQLParser.RealTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldLength.
    def visitFieldLength(self, ctx: SQLParser.FieldLengthContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldOptions.
    def visitFieldOptions(self, ctx: SQLParser.FieldOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#charsetWithOptBinary.
    def visitCharsetWithOptBinary(self, ctx: SQLParser.CharsetWithOptBinaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ascii.
    def visitAscii(self, ctx: SQLParser.AsciiContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#unicode.
    def visitUnicode(self, ctx: SQLParser.UnicodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#wsNumCodepoints.
    def visitWsNumCodepoints(self, ctx: SQLParser.WsNumCodepointsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#typeDatetimePrecision.
    def visitTypeDatetimePrecision(self, ctx: SQLParser.TypeDatetimePrecisionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#charsetName.
    def visitCharsetName(self, ctx: SQLParser.CharsetNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#collationName.
    def visitCollationName(self, ctx: SQLParser.CollationNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTableOptions.
    def visitCreateTableOptions(self, ctx: SQLParser.CreateTableOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTableOptionsSpaceSeparated.
    def visitCreateTableOptionsSpaceSeparated(
        self, ctx: SQLParser.CreateTableOptionsSpaceSeparatedContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createTableOption.
    def visitCreateTableOption(self, ctx: SQLParser.CreateTableOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ternaryOption.
    def visitTernaryOption(self, ctx: SQLParser.TernaryOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#defaultCollation.
    def visitDefaultCollation(self, ctx: SQLParser.DefaultCollationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#defaultEncryption.
    def visitDefaultEncryption(self, ctx: SQLParser.DefaultEncryptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#defaultCharset.
    def visitDefaultCharset(self, ctx: SQLParser.DefaultCharsetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionClause.
    def visitPartitionClause(self, ctx: SQLParser.PartitionClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDefKey.
    def visitPartitionDefKey(self, ctx: SQLParser.PartitionDefKeyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDefHash.
    def visitPartitionDefHash(self, ctx: SQLParser.PartitionDefHashContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDefRangeList.
    def visitPartitionDefRangeList(self, ctx: SQLParser.PartitionDefRangeListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#subPartitions.
    def visitSubPartitions(self, ctx: SQLParser.SubPartitionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionKeyAlgorithm.
    def visitPartitionKeyAlgorithm(self, ctx: SQLParser.PartitionKeyAlgorithmContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDefinitions.
    def visitPartitionDefinitions(self, ctx: SQLParser.PartitionDefinitionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionDefinition.
    def visitPartitionDefinition(self, ctx: SQLParser.PartitionDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionValuesIn.
    def visitPartitionValuesIn(self, ctx: SQLParser.PartitionValuesInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionOption.
    def visitPartitionOption(self, ctx: SQLParser.PartitionOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#subpartitionDefinition.
    def visitSubpartitionDefinition(self, ctx: SQLParser.SubpartitionDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionValueItemListParen.
    def visitPartitionValueItemListParen(
        self, ctx: SQLParser.PartitionValueItemListParenContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#partitionValueItem.
    def visitPartitionValueItem(self, ctx: SQLParser.PartitionValueItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#definerClause.
    def visitDefinerClause(self, ctx: SQLParser.DefinerClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ifExists.
    def visitIfExists(self, ctx: SQLParser.IfExistsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ifNotExists.
    def visitIfNotExists(self, ctx: SQLParser.IfNotExistsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#procedureParameter.
    def visitProcedureParameter(self, ctx: SQLParser.ProcedureParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#functionParameter.
    def visitFunctionParameter(self, ctx: SQLParser.FunctionParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#collate.
    def visitCollate(self, ctx: SQLParser.CollateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#typeWithOptCollate.
    def visitTypeWithOptCollate(self, ctx: SQLParser.TypeWithOptCollateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#schemaIdentifierPair.
    def visitSchemaIdentifierPair(self, ctx: SQLParser.SchemaIdentifierPairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewRefList.
    def visitViewRefList(self, ctx: SQLParser.ViewRefListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#updateList.
    def visitUpdateList(self, ctx: SQLParser.UpdateListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#updateElement.
    def visitUpdateElement(self, ctx: SQLParser.UpdateElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#charsetClause.
    def visitCharsetClause(self, ctx: SQLParser.CharsetClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldsClause.
    def visitFieldsClause(self, ctx: SQLParser.FieldsClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldTerm.
    def visitFieldTerm(self, ctx: SQLParser.FieldTermContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#linesClause.
    def visitLinesClause(self, ctx: SQLParser.LinesClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lineTerm.
    def visitLineTerm(self, ctx: SQLParser.LineTermContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#userList.
    def visitUserList(self, ctx: SQLParser.UserListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUserList.
    def visitCreateUserList(self, ctx: SQLParser.CreateUserListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterUserList.
    def visitAlterUserList(self, ctx: SQLParser.AlterUserListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#createUserEntry.
    def visitCreateUserEntry(self, ctx: SQLParser.CreateUserEntryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#alterUserEntry.
    def visitAlterUserEntry(self, ctx: SQLParser.AlterUserEntryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#retainCurrentPassword.
    def visitRetainCurrentPassword(self, ctx: SQLParser.RetainCurrentPasswordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#discardOldPassword.
    def visitDiscardOldPassword(self, ctx: SQLParser.DiscardOldPasswordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#replacePassword.
    def visitReplacePassword(self, ctx: SQLParser.ReplacePasswordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#userIdentifierOrText.
    def visitUserIdentifierOrText(self, ctx: SQLParser.UserIdentifierOrTextContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#user.
    def visitUser(self, ctx: SQLParser.UserContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#likeClause.
    def visitLikeClause(self, ctx: SQLParser.LikeClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#likeOrWhere.
    def visitLikeOrWhere(self, ctx: SQLParser.LikeOrWhereContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#onlineOption.
    def visitOnlineOption(self, ctx: SQLParser.OnlineOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#noWriteToBinLog.
    def visitNoWriteToBinLog(self, ctx: SQLParser.NoWriteToBinLogContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#usePartition.
    def visitUsePartition(self, ctx: SQLParser.UsePartitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#fieldIdentifier.
    def visitFieldIdentifier(self, ctx: SQLParser.FieldIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnName.
    def visitColumnName(self, ctx: SQLParser.ColumnNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnInternalRef.
    def visitColumnInternalRef(self, ctx: SQLParser.ColumnInternalRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnInternalRefList.
    def visitColumnInternalRefList(self, ctx: SQLParser.ColumnInternalRefListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#columnRef.
    def visitColumnRef(self, ctx: SQLParser.ColumnRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#insertIdentifier.
    def visitInsertIdentifier(self, ctx: SQLParser.InsertIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexName.
    def visitIndexName(self, ctx: SQLParser.IndexNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#indexRef.
    def visitIndexRef(self, ctx: SQLParser.IndexRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableWild.
    def visitTableWild(self, ctx: SQLParser.TableWildContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#schemaName.
    def visitSchemaName(self, ctx: SQLParser.SchemaNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#schemaRef.
    def visitSchemaRef(self, ctx: SQLParser.SchemaRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#procedureName.
    def visitProcedureName(self, ctx: SQLParser.ProcedureNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#procedureRef.
    def visitProcedureRef(self, ctx: SQLParser.ProcedureRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#functionName.
    def visitFunctionName(self, ctx: SQLParser.FunctionNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#functionRef.
    def visitFunctionRef(self, ctx: SQLParser.FunctionRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#triggerName.
    def visitTriggerName(self, ctx: SQLParser.TriggerNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#triggerRef.
    def visitTriggerRef(self, ctx: SQLParser.TriggerRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewName.
    def visitViewName(self, ctx: SQLParser.ViewNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#viewRef.
    def visitViewRef(self, ctx: SQLParser.ViewRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tablespaceName.
    def visitTablespaceName(self, ctx: SQLParser.TablespaceNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tablespaceRef.
    def visitTablespaceRef(self, ctx: SQLParser.TablespaceRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#logfileGroupName.
    def visitLogfileGroupName(self, ctx: SQLParser.LogfileGroupNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#logfileGroupRef.
    def visitLogfileGroupRef(self, ctx: SQLParser.LogfileGroupRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#eventName.
    def visitEventName(self, ctx: SQLParser.EventNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#eventRef.
    def visitEventRef(self, ctx: SQLParser.EventRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#udfName.
    def visitUdfName(self, ctx: SQLParser.UdfNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#serverName.
    def visitServerName(self, ctx: SQLParser.ServerNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#serverRef.
    def visitServerRef(self, ctx: SQLParser.ServerRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#engineRef.
    def visitEngineRef(self, ctx: SQLParser.EngineRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableName.
    def visitTableName(self, ctx: SQLParser.TableNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#filterTableRef.
    def visitFilterTableRef(self, ctx: SQLParser.FilterTableRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableRefWithWildcard.
    def visitTableRefWithWildcard(self, ctx: SQLParser.TableRefWithWildcardContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableRef.
    def visitTableRef(self, ctx: SQLParser.TableRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableRefList.
    def visitTableRefList(self, ctx: SQLParser.TableRefListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#tableAliasRefList.
    def visitTableAliasRefList(self, ctx: SQLParser.TableAliasRefListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#parameterName.
    def visitParameterName(self, ctx: SQLParser.ParameterNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#labelIdentifier.
    def visitLabelIdentifier(self, ctx: SQLParser.LabelIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#labelRef.
    def visitLabelRef(self, ctx: SQLParser.LabelRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleIdentifier.
    def visitRoleIdentifier(self, ctx: SQLParser.RoleIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleRef.
    def visitRoleRef(self, ctx: SQLParser.RoleRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#pluginRef.
    def visitPluginRef(self, ctx: SQLParser.PluginRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#componentRef.
    def visitComponentRef(self, ctx: SQLParser.ComponentRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#resourceGroupRef.
    def visitResourceGroupRef(self, ctx: SQLParser.ResourceGroupRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#windowName.
    def visitWindowName(self, ctx: SQLParser.WindowNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#pureIdentifier.
    def visitPureIdentifier(self, ctx: SQLParser.PureIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifier.
    def visitIdentifier(self, ctx: SQLParser.IdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierList.
    def visitIdentifierList(self, ctx: SQLParser.IdentifierListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierListWithParentheses.
    def visitIdentifierListWithParentheses(
        self, ctx: SQLParser.IdentifierListWithParenthesesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#qualifiedIdentifier.
    def visitQualifiedIdentifier(self, ctx: SQLParser.QualifiedIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#simpleIdentifier.
    def visitSimpleIdentifier(self, ctx: SQLParser.SimpleIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#dotIdentifier.
    def visitDotIdentifier(self, ctx: SQLParser.DotIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ulong_number.
    def visitUlong_number(self, ctx: SQLParser.Ulong_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#real_ulong_number.
    def visitReal_ulong_number(self, ctx: SQLParser.Real_ulong_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#ulonglong_number.
    def visitUlonglong_number(self, ctx: SQLParser.Ulonglong_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#real_ulonglong_number.
    def visitReal_ulonglong_number(self, ctx: SQLParser.Real_ulonglong_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#literal.
    def visitLiteral(self, ctx: SQLParser.LiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#signedLiteral.
    def visitSignedLiteral(self, ctx: SQLParser.SignedLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#stringList.
    def visitStringList(self, ctx: SQLParser.StringListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textStringLiteral.
    def visitTextStringLiteral(self, ctx: SQLParser.TextStringLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textString.
    def visitTextString(self, ctx: SQLParser.TextStringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textStringHash.
    def visitTextStringHash(self, ctx: SQLParser.TextStringHashContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textLiteral.
    def visitTextLiteral(self, ctx: SQLParser.TextLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textStringNoLinebreak.
    def visitTextStringNoLinebreak(self, ctx: SQLParser.TextStringNoLinebreakContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textStringLiteralList.
    def visitTextStringLiteralList(self, ctx: SQLParser.TextStringLiteralListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#numLiteral.
    def visitNumLiteral(self, ctx: SQLParser.NumLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#boolLiteral.
    def visitBoolLiteral(self, ctx: SQLParser.BoolLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#nullLiteral.
    def visitNullLiteral(self, ctx: SQLParser.NullLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#temporalLiteral.
    def visitTemporalLiteral(self, ctx: SQLParser.TemporalLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#floatOptions.
    def visitFloatOptions(self, ctx: SQLParser.FloatOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#standardFloatOptions.
    def visitStandardFloatOptions(self, ctx: SQLParser.StandardFloatOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#precision.
    def visitPrecision(self, ctx: SQLParser.PrecisionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#textOrIdentifier.
    def visitTextOrIdentifier(self, ctx: SQLParser.TextOrIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lValueIdentifier.
    def visitLValueIdentifier(self, ctx: SQLParser.LValueIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleIdentifierOrText.
    def visitRoleIdentifierOrText(self, ctx: SQLParser.RoleIdentifierOrTextContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#sizeNumber.
    def visitSizeNumber(self, ctx: SQLParser.SizeNumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#parentheses.
    def visitParentheses(self, ctx: SQLParser.ParenthesesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#equal.
    def visitEqual(self, ctx: SQLParser.EqualContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#optionType.
    def visitOptionType(self, ctx: SQLParser.OptionTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#varIdentType.
    def visitVarIdentType(self, ctx: SQLParser.VarIdentTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#setVarIdentType.
    def visitSetVarIdentType(self, ctx: SQLParser.SetVarIdentTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeyword.
    def visitIdentifierKeyword(self, ctx: SQLParser.IdentifierKeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeywordsAmbiguous1RolesAndLabels.
    def visitIdentifierKeywordsAmbiguous1RolesAndLabels(
        self, ctx: SQLParser.IdentifierKeywordsAmbiguous1RolesAndLabelsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeywordsAmbiguous2Labels.
    def visitIdentifierKeywordsAmbiguous2Labels(
        self, ctx: SQLParser.IdentifierKeywordsAmbiguous2LabelsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#labelKeyword.
    def visitLabelKeyword(self, ctx: SQLParser.LabelKeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeywordsAmbiguous3Roles.
    def visitIdentifierKeywordsAmbiguous3Roles(
        self, ctx: SQLParser.IdentifierKeywordsAmbiguous3RolesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeywordsUnambiguous.
    def visitIdentifierKeywordsUnambiguous(
        self, ctx: SQLParser.IdentifierKeywordsUnambiguousContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleKeyword.
    def visitRoleKeyword(self, ctx: SQLParser.RoleKeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#lValueKeyword.
    def visitLValueKeyword(self, ctx: SQLParser.LValueKeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#identifierKeywordsAmbiguous4SystemVariables.
    def visitIdentifierKeywordsAmbiguous4SystemVariables(
        self, ctx: SQLParser.IdentifierKeywordsAmbiguous4SystemVariablesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleOrIdentifierKeyword.
    def visitRoleOrIdentifierKeyword(
        self, ctx: SQLParser.RoleOrIdentifierKeywordContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SQLParser#roleOrLabelKeyword.
    def visitRoleOrLabelKeyword(self, ctx: SQLParser.RoleOrLabelKeywordContext):
        return self.visitChildren(ctx)


del SQLParser
