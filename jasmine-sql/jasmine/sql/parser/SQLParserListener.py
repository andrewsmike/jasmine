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


# This class defines a complete listener for a parse tree produced by SQLParser.
class SQLParserListener(ParseTreeListener):

    # Enter a parse tree produced by SQLParser#sqlProgram.
    def enterSqlProgram(self, ctx:SQLParser.SqlProgramContext):
        pass

    # Exit a parse tree produced by SQLParser#sqlProgram.
    def exitSqlProgram(self, ctx:SQLParser.SqlProgramContext):
        pass


    # Enter a parse tree produced by SQLParser#statement.
    def enterStatement(self, ctx:SQLParser.StatementContext):
        pass

    # Exit a parse tree produced by SQLParser#statement.
    def exitStatement(self, ctx:SQLParser.StatementContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleStatement.
    def enterSimpleStatement(self, ctx:SQLParser.SimpleStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleStatement.
    def exitSimpleStatement(self, ctx:SQLParser.SimpleStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#alterStatement.
    def enterAlterStatement(self, ctx:SQLParser.AlterStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#alterStatement.
    def exitAlterStatement(self, ctx:SQLParser.AlterStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#alterDatabase.
    def enterAlterDatabase(self, ctx:SQLParser.AlterDatabaseContext):
        pass

    # Exit a parse tree produced by SQLParser#alterDatabase.
    def exitAlterDatabase(self, ctx:SQLParser.AlterDatabaseContext):
        pass


    # Enter a parse tree produced by SQLParser#alterEvent.
    def enterAlterEvent(self, ctx:SQLParser.AlterEventContext):
        pass

    # Exit a parse tree produced by SQLParser#alterEvent.
    def exitAlterEvent(self, ctx:SQLParser.AlterEventContext):
        pass


    # Enter a parse tree produced by SQLParser#alterLogfileGroup.
    def enterAlterLogfileGroup(self, ctx:SQLParser.AlterLogfileGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#alterLogfileGroup.
    def exitAlterLogfileGroup(self, ctx:SQLParser.AlterLogfileGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#alterLogfileGroupOptions.
    def enterAlterLogfileGroupOptions(self, ctx:SQLParser.AlterLogfileGroupOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#alterLogfileGroupOptions.
    def exitAlterLogfileGroupOptions(self, ctx:SQLParser.AlterLogfileGroupOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#alterLogfileGroupOption.
    def enterAlterLogfileGroupOption(self, ctx:SQLParser.AlterLogfileGroupOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#alterLogfileGroupOption.
    def exitAlterLogfileGroupOption(self, ctx:SQLParser.AlterLogfileGroupOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#alterServer.
    def enterAlterServer(self, ctx:SQLParser.AlterServerContext):
        pass

    # Exit a parse tree produced by SQLParser#alterServer.
    def exitAlterServer(self, ctx:SQLParser.AlterServerContext):
        pass


    # Enter a parse tree produced by SQLParser#alterTable.
    def enterAlterTable(self, ctx:SQLParser.AlterTableContext):
        pass

    # Exit a parse tree produced by SQLParser#alterTable.
    def exitAlterTable(self, ctx:SQLParser.AlterTableContext):
        pass


    # Enter a parse tree produced by SQLParser#alterTableActions.
    def enterAlterTableActions(self, ctx:SQLParser.AlterTableActionsContext):
        pass

    # Exit a parse tree produced by SQLParser#alterTableActions.
    def exitAlterTableActions(self, ctx:SQLParser.AlterTableActionsContext):
        pass


    # Enter a parse tree produced by SQLParser#alterCommandList.
    def enterAlterCommandList(self, ctx:SQLParser.AlterCommandListContext):
        pass

    # Exit a parse tree produced by SQLParser#alterCommandList.
    def exitAlterCommandList(self, ctx:SQLParser.AlterCommandListContext):
        pass


    # Enter a parse tree produced by SQLParser#alterCommandsModifierList.
    def enterAlterCommandsModifierList(self, ctx:SQLParser.AlterCommandsModifierListContext):
        pass

    # Exit a parse tree produced by SQLParser#alterCommandsModifierList.
    def exitAlterCommandsModifierList(self, ctx:SQLParser.AlterCommandsModifierListContext):
        pass


    # Enter a parse tree produced by SQLParser#standaloneAlterCommands.
    def enterStandaloneAlterCommands(self, ctx:SQLParser.StandaloneAlterCommandsContext):
        pass

    # Exit a parse tree produced by SQLParser#standaloneAlterCommands.
    def exitStandaloneAlterCommands(self, ctx:SQLParser.StandaloneAlterCommandsContext):
        pass


    # Enter a parse tree produced by SQLParser#alterPartition.
    def enterAlterPartition(self, ctx:SQLParser.AlterPartitionContext):
        pass

    # Exit a parse tree produced by SQLParser#alterPartition.
    def exitAlterPartition(self, ctx:SQLParser.AlterPartitionContext):
        pass


    # Enter a parse tree produced by SQLParser#alterList.
    def enterAlterList(self, ctx:SQLParser.AlterListContext):
        pass

    # Exit a parse tree produced by SQLParser#alterList.
    def exitAlterList(self, ctx:SQLParser.AlterListContext):
        pass


    # Enter a parse tree produced by SQLParser#alterCommandsModifier.
    def enterAlterCommandsModifier(self, ctx:SQLParser.AlterCommandsModifierContext):
        pass

    # Exit a parse tree produced by SQLParser#alterCommandsModifier.
    def exitAlterCommandsModifier(self, ctx:SQLParser.AlterCommandsModifierContext):
        pass


    # Enter a parse tree produced by SQLParser#alterListItem.
    def enterAlterListItem(self, ctx:SQLParser.AlterListItemContext):
        pass

    # Exit a parse tree produced by SQLParser#alterListItem.
    def exitAlterListItem(self, ctx:SQLParser.AlterListItemContext):
        pass


    # Enter a parse tree produced by SQLParser#place.
    def enterPlace(self, ctx:SQLParser.PlaceContext):
        pass

    # Exit a parse tree produced by SQLParser#place.
    def exitPlace(self, ctx:SQLParser.PlaceContext):
        pass


    # Enter a parse tree produced by SQLParser#restrict.
    def enterRestrict(self, ctx:SQLParser.RestrictContext):
        pass

    # Exit a parse tree produced by SQLParser#restrict.
    def exitRestrict(self, ctx:SQLParser.RestrictContext):
        pass


    # Enter a parse tree produced by SQLParser#alterOrderList.
    def enterAlterOrderList(self, ctx:SQLParser.AlterOrderListContext):
        pass

    # Exit a parse tree produced by SQLParser#alterOrderList.
    def exitAlterOrderList(self, ctx:SQLParser.AlterOrderListContext):
        pass


    # Enter a parse tree produced by SQLParser#alterAlgorithmOption.
    def enterAlterAlgorithmOption(self, ctx:SQLParser.AlterAlgorithmOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#alterAlgorithmOption.
    def exitAlterAlgorithmOption(self, ctx:SQLParser.AlterAlgorithmOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#alterLockOption.
    def enterAlterLockOption(self, ctx:SQLParser.AlterLockOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#alterLockOption.
    def exitAlterLockOption(self, ctx:SQLParser.AlterLockOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#indexLockAndAlgorithm.
    def enterIndexLockAndAlgorithm(self, ctx:SQLParser.IndexLockAndAlgorithmContext):
        pass

    # Exit a parse tree produced by SQLParser#indexLockAndAlgorithm.
    def exitIndexLockAndAlgorithm(self, ctx:SQLParser.IndexLockAndAlgorithmContext):
        pass


    # Enter a parse tree produced by SQLParser#withValidation.
    def enterWithValidation(self, ctx:SQLParser.WithValidationContext):
        pass

    # Exit a parse tree produced by SQLParser#withValidation.
    def exitWithValidation(self, ctx:SQLParser.WithValidationContext):
        pass


    # Enter a parse tree produced by SQLParser#removePartitioning.
    def enterRemovePartitioning(self, ctx:SQLParser.RemovePartitioningContext):
        pass

    # Exit a parse tree produced by SQLParser#removePartitioning.
    def exitRemovePartitioning(self, ctx:SQLParser.RemovePartitioningContext):
        pass


    # Enter a parse tree produced by SQLParser#allOrPartitionNameList.
    def enterAllOrPartitionNameList(self, ctx:SQLParser.AllOrPartitionNameListContext):
        pass

    # Exit a parse tree produced by SQLParser#allOrPartitionNameList.
    def exitAllOrPartitionNameList(self, ctx:SQLParser.AllOrPartitionNameListContext):
        pass


    # Enter a parse tree produced by SQLParser#alterTablespace.
    def enterAlterTablespace(self, ctx:SQLParser.AlterTablespaceContext):
        pass

    # Exit a parse tree produced by SQLParser#alterTablespace.
    def exitAlterTablespace(self, ctx:SQLParser.AlterTablespaceContext):
        pass


    # Enter a parse tree produced by SQLParser#alterUndoTablespace.
    def enterAlterUndoTablespace(self, ctx:SQLParser.AlterUndoTablespaceContext):
        pass

    # Exit a parse tree produced by SQLParser#alterUndoTablespace.
    def exitAlterUndoTablespace(self, ctx:SQLParser.AlterUndoTablespaceContext):
        pass


    # Enter a parse tree produced by SQLParser#undoTableSpaceOptions.
    def enterUndoTableSpaceOptions(self, ctx:SQLParser.UndoTableSpaceOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#undoTableSpaceOptions.
    def exitUndoTableSpaceOptions(self, ctx:SQLParser.UndoTableSpaceOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#undoTableSpaceOption.
    def enterUndoTableSpaceOption(self, ctx:SQLParser.UndoTableSpaceOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#undoTableSpaceOption.
    def exitUndoTableSpaceOption(self, ctx:SQLParser.UndoTableSpaceOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#alterTablespaceOptions.
    def enterAlterTablespaceOptions(self, ctx:SQLParser.AlterTablespaceOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#alterTablespaceOptions.
    def exitAlterTablespaceOptions(self, ctx:SQLParser.AlterTablespaceOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#alterTablespaceOption.
    def enterAlterTablespaceOption(self, ctx:SQLParser.AlterTablespaceOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#alterTablespaceOption.
    def exitAlterTablespaceOption(self, ctx:SQLParser.AlterTablespaceOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#changeTablespaceOption.
    def enterChangeTablespaceOption(self, ctx:SQLParser.ChangeTablespaceOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#changeTablespaceOption.
    def exitChangeTablespaceOption(self, ctx:SQLParser.ChangeTablespaceOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#alterView.
    def enterAlterView(self, ctx:SQLParser.AlterViewContext):
        pass

    # Exit a parse tree produced by SQLParser#alterView.
    def exitAlterView(self, ctx:SQLParser.AlterViewContext):
        pass


    # Enter a parse tree produced by SQLParser#viewTail.
    def enterViewTail(self, ctx:SQLParser.ViewTailContext):
        pass

    # Exit a parse tree produced by SQLParser#viewTail.
    def exitViewTail(self, ctx:SQLParser.ViewTailContext):
        pass


    # Enter a parse tree produced by SQLParser#viewSelect.
    def enterViewSelect(self, ctx:SQLParser.ViewSelectContext):
        pass

    # Exit a parse tree produced by SQLParser#viewSelect.
    def exitViewSelect(self, ctx:SQLParser.ViewSelectContext):
        pass


    # Enter a parse tree produced by SQLParser#viewCheckOption.
    def enterViewCheckOption(self, ctx:SQLParser.ViewCheckOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#viewCheckOption.
    def exitViewCheckOption(self, ctx:SQLParser.ViewCheckOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createStatement.
    def enterCreateStatement(self, ctx:SQLParser.CreateStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#createStatement.
    def exitCreateStatement(self, ctx:SQLParser.CreateStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#createDatabase.
    def enterCreateDatabase(self, ctx:SQLParser.CreateDatabaseContext):
        pass

    # Exit a parse tree produced by SQLParser#createDatabase.
    def exitCreateDatabase(self, ctx:SQLParser.CreateDatabaseContext):
        pass


    # Enter a parse tree produced by SQLParser#createDatabaseOption.
    def enterCreateDatabaseOption(self, ctx:SQLParser.CreateDatabaseOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#createDatabaseOption.
    def exitCreateDatabaseOption(self, ctx:SQLParser.CreateDatabaseOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createTable.
    def enterCreateTable(self, ctx:SQLParser.CreateTableContext):
        pass

    # Exit a parse tree produced by SQLParser#createTable.
    def exitCreateTable(self, ctx:SQLParser.CreateTableContext):
        pass


    # Enter a parse tree produced by SQLParser#tableElementList.
    def enterTableElementList(self, ctx:SQLParser.TableElementListContext):
        pass

    # Exit a parse tree produced by SQLParser#tableElementList.
    def exitTableElementList(self, ctx:SQLParser.TableElementListContext):
        pass


    # Enter a parse tree produced by SQLParser#tableElement.
    def enterTableElement(self, ctx:SQLParser.TableElementContext):
        pass

    # Exit a parse tree produced by SQLParser#tableElement.
    def exitTableElement(self, ctx:SQLParser.TableElementContext):
        pass


    # Enter a parse tree produced by SQLParser#duplicateAsQueryExpression.
    def enterDuplicateAsQueryExpression(self, ctx:SQLParser.DuplicateAsQueryExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#duplicateAsQueryExpression.
    def exitDuplicateAsQueryExpression(self, ctx:SQLParser.DuplicateAsQueryExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#queryExpressionOrParens.
    def enterQueryExpressionOrParens(self, ctx:SQLParser.QueryExpressionOrParensContext):
        pass

    # Exit a parse tree produced by SQLParser#queryExpressionOrParens.
    def exitQueryExpressionOrParens(self, ctx:SQLParser.QueryExpressionOrParensContext):
        pass


    # Enter a parse tree produced by SQLParser#createRoutine.
    def enterCreateRoutine(self, ctx:SQLParser.CreateRoutineContext):
        pass

    # Exit a parse tree produced by SQLParser#createRoutine.
    def exitCreateRoutine(self, ctx:SQLParser.CreateRoutineContext):
        pass


    # Enter a parse tree produced by SQLParser#createProcedure.
    def enterCreateProcedure(self, ctx:SQLParser.CreateProcedureContext):
        pass

    # Exit a parse tree produced by SQLParser#createProcedure.
    def exitCreateProcedure(self, ctx:SQLParser.CreateProcedureContext):
        pass


    # Enter a parse tree produced by SQLParser#createFunction.
    def enterCreateFunction(self, ctx:SQLParser.CreateFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#createFunction.
    def exitCreateFunction(self, ctx:SQLParser.CreateFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#createUdf.
    def enterCreateUdf(self, ctx:SQLParser.CreateUdfContext):
        pass

    # Exit a parse tree produced by SQLParser#createUdf.
    def exitCreateUdf(self, ctx:SQLParser.CreateUdfContext):
        pass


    # Enter a parse tree produced by SQLParser#routineCreateOption.
    def enterRoutineCreateOption(self, ctx:SQLParser.RoutineCreateOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#routineCreateOption.
    def exitRoutineCreateOption(self, ctx:SQLParser.RoutineCreateOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#routineAlterOptions.
    def enterRoutineAlterOptions(self, ctx:SQLParser.RoutineAlterOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#routineAlterOptions.
    def exitRoutineAlterOptions(self, ctx:SQLParser.RoutineAlterOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#routineOption.
    def enterRoutineOption(self, ctx:SQLParser.RoutineOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#routineOption.
    def exitRoutineOption(self, ctx:SQLParser.RoutineOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createIndex.
    def enterCreateIndex(self, ctx:SQLParser.CreateIndexContext):
        pass

    # Exit a parse tree produced by SQLParser#createIndex.
    def exitCreateIndex(self, ctx:SQLParser.CreateIndexContext):
        pass


    # Enter a parse tree produced by SQLParser#indexNameAndType.
    def enterIndexNameAndType(self, ctx:SQLParser.IndexNameAndTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#indexNameAndType.
    def exitIndexNameAndType(self, ctx:SQLParser.IndexNameAndTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#createIndexTarget.
    def enterCreateIndexTarget(self, ctx:SQLParser.CreateIndexTargetContext):
        pass

    # Exit a parse tree produced by SQLParser#createIndexTarget.
    def exitCreateIndexTarget(self, ctx:SQLParser.CreateIndexTargetContext):
        pass


    # Enter a parse tree produced by SQLParser#createLogfileGroup.
    def enterCreateLogfileGroup(self, ctx:SQLParser.CreateLogfileGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#createLogfileGroup.
    def exitCreateLogfileGroup(self, ctx:SQLParser.CreateLogfileGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#logfileGroupOptions.
    def enterLogfileGroupOptions(self, ctx:SQLParser.LogfileGroupOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#logfileGroupOptions.
    def exitLogfileGroupOptions(self, ctx:SQLParser.LogfileGroupOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#logfileGroupOption.
    def enterLogfileGroupOption(self, ctx:SQLParser.LogfileGroupOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#logfileGroupOption.
    def exitLogfileGroupOption(self, ctx:SQLParser.LogfileGroupOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createServer.
    def enterCreateServer(self, ctx:SQLParser.CreateServerContext):
        pass

    # Exit a parse tree produced by SQLParser#createServer.
    def exitCreateServer(self, ctx:SQLParser.CreateServerContext):
        pass


    # Enter a parse tree produced by SQLParser#serverOptions.
    def enterServerOptions(self, ctx:SQLParser.ServerOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#serverOptions.
    def exitServerOptions(self, ctx:SQLParser.ServerOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#serverOption.
    def enterServerOption(self, ctx:SQLParser.ServerOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#serverOption.
    def exitServerOption(self, ctx:SQLParser.ServerOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createTablespace.
    def enterCreateTablespace(self, ctx:SQLParser.CreateTablespaceContext):
        pass

    # Exit a parse tree produced by SQLParser#createTablespace.
    def exitCreateTablespace(self, ctx:SQLParser.CreateTablespaceContext):
        pass


    # Enter a parse tree produced by SQLParser#createUndoTablespace.
    def enterCreateUndoTablespace(self, ctx:SQLParser.CreateUndoTablespaceContext):
        pass

    # Exit a parse tree produced by SQLParser#createUndoTablespace.
    def exitCreateUndoTablespace(self, ctx:SQLParser.CreateUndoTablespaceContext):
        pass


    # Enter a parse tree produced by SQLParser#tsDataFileName.
    def enterTsDataFileName(self, ctx:SQLParser.TsDataFileNameContext):
        pass

    # Exit a parse tree produced by SQLParser#tsDataFileName.
    def exitTsDataFileName(self, ctx:SQLParser.TsDataFileNameContext):
        pass


    # Enter a parse tree produced by SQLParser#tsDataFile.
    def enterTsDataFile(self, ctx:SQLParser.TsDataFileContext):
        pass

    # Exit a parse tree produced by SQLParser#tsDataFile.
    def exitTsDataFile(self, ctx:SQLParser.TsDataFileContext):
        pass


    # Enter a parse tree produced by SQLParser#tablespaceOptions.
    def enterTablespaceOptions(self, ctx:SQLParser.TablespaceOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#tablespaceOptions.
    def exitTablespaceOptions(self, ctx:SQLParser.TablespaceOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#tablespaceOption.
    def enterTablespaceOption(self, ctx:SQLParser.TablespaceOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#tablespaceOption.
    def exitTablespaceOption(self, ctx:SQLParser.TablespaceOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionInitialSize.
    def enterTsOptionInitialSize(self, ctx:SQLParser.TsOptionInitialSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionInitialSize.
    def exitTsOptionInitialSize(self, ctx:SQLParser.TsOptionInitialSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionUndoRedoBufferSize.
    def enterTsOptionUndoRedoBufferSize(self, ctx:SQLParser.TsOptionUndoRedoBufferSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionUndoRedoBufferSize.
    def exitTsOptionUndoRedoBufferSize(self, ctx:SQLParser.TsOptionUndoRedoBufferSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionAutoextendSize.
    def enterTsOptionAutoextendSize(self, ctx:SQLParser.TsOptionAutoextendSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionAutoextendSize.
    def exitTsOptionAutoextendSize(self, ctx:SQLParser.TsOptionAutoextendSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionMaxSize.
    def enterTsOptionMaxSize(self, ctx:SQLParser.TsOptionMaxSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionMaxSize.
    def exitTsOptionMaxSize(self, ctx:SQLParser.TsOptionMaxSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionExtentSize.
    def enterTsOptionExtentSize(self, ctx:SQLParser.TsOptionExtentSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionExtentSize.
    def exitTsOptionExtentSize(self, ctx:SQLParser.TsOptionExtentSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionNodegroup.
    def enterTsOptionNodegroup(self, ctx:SQLParser.TsOptionNodegroupContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionNodegroup.
    def exitTsOptionNodegroup(self, ctx:SQLParser.TsOptionNodegroupContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionEngine.
    def enterTsOptionEngine(self, ctx:SQLParser.TsOptionEngineContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionEngine.
    def exitTsOptionEngine(self, ctx:SQLParser.TsOptionEngineContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionWait.
    def enterTsOptionWait(self, ctx:SQLParser.TsOptionWaitContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionWait.
    def exitTsOptionWait(self, ctx:SQLParser.TsOptionWaitContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionComment.
    def enterTsOptionComment(self, ctx:SQLParser.TsOptionCommentContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionComment.
    def exitTsOptionComment(self, ctx:SQLParser.TsOptionCommentContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionFileblockSize.
    def enterTsOptionFileblockSize(self, ctx:SQLParser.TsOptionFileblockSizeContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionFileblockSize.
    def exitTsOptionFileblockSize(self, ctx:SQLParser.TsOptionFileblockSizeContext):
        pass


    # Enter a parse tree produced by SQLParser#tsOptionEncryption.
    def enterTsOptionEncryption(self, ctx:SQLParser.TsOptionEncryptionContext):
        pass

    # Exit a parse tree produced by SQLParser#tsOptionEncryption.
    def exitTsOptionEncryption(self, ctx:SQLParser.TsOptionEncryptionContext):
        pass


    # Enter a parse tree produced by SQLParser#createView.
    def enterCreateView(self, ctx:SQLParser.CreateViewContext):
        pass

    # Exit a parse tree produced by SQLParser#createView.
    def exitCreateView(self, ctx:SQLParser.CreateViewContext):
        pass


    # Enter a parse tree produced by SQLParser#viewReplaceOrAlgorithm.
    def enterViewReplaceOrAlgorithm(self, ctx:SQLParser.ViewReplaceOrAlgorithmContext):
        pass

    # Exit a parse tree produced by SQLParser#viewReplaceOrAlgorithm.
    def exitViewReplaceOrAlgorithm(self, ctx:SQLParser.ViewReplaceOrAlgorithmContext):
        pass


    # Enter a parse tree produced by SQLParser#viewAlgorithm.
    def enterViewAlgorithm(self, ctx:SQLParser.ViewAlgorithmContext):
        pass

    # Exit a parse tree produced by SQLParser#viewAlgorithm.
    def exitViewAlgorithm(self, ctx:SQLParser.ViewAlgorithmContext):
        pass


    # Enter a parse tree produced by SQLParser#viewSuid.
    def enterViewSuid(self, ctx:SQLParser.ViewSuidContext):
        pass

    # Exit a parse tree produced by SQLParser#viewSuid.
    def exitViewSuid(self, ctx:SQLParser.ViewSuidContext):
        pass


    # Enter a parse tree produced by SQLParser#createTrigger.
    def enterCreateTrigger(self, ctx:SQLParser.CreateTriggerContext):
        pass

    # Exit a parse tree produced by SQLParser#createTrigger.
    def exitCreateTrigger(self, ctx:SQLParser.CreateTriggerContext):
        pass


    # Enter a parse tree produced by SQLParser#triggerFollowsPrecedesClause.
    def enterTriggerFollowsPrecedesClause(self, ctx:SQLParser.TriggerFollowsPrecedesClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#triggerFollowsPrecedesClause.
    def exitTriggerFollowsPrecedesClause(self, ctx:SQLParser.TriggerFollowsPrecedesClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#createEvent.
    def enterCreateEvent(self, ctx:SQLParser.CreateEventContext):
        pass

    # Exit a parse tree produced by SQLParser#createEvent.
    def exitCreateEvent(self, ctx:SQLParser.CreateEventContext):
        pass


    # Enter a parse tree produced by SQLParser#createRole.
    def enterCreateRole(self, ctx:SQLParser.CreateRoleContext):
        pass

    # Exit a parse tree produced by SQLParser#createRole.
    def exitCreateRole(self, ctx:SQLParser.CreateRoleContext):
        pass


    # Enter a parse tree produced by SQLParser#createSpatialReference.
    def enterCreateSpatialReference(self, ctx:SQLParser.CreateSpatialReferenceContext):
        pass

    # Exit a parse tree produced by SQLParser#createSpatialReference.
    def exitCreateSpatialReference(self, ctx:SQLParser.CreateSpatialReferenceContext):
        pass


    # Enter a parse tree produced by SQLParser#srsAttribute.
    def enterSrsAttribute(self, ctx:SQLParser.SrsAttributeContext):
        pass

    # Exit a parse tree produced by SQLParser#srsAttribute.
    def exitSrsAttribute(self, ctx:SQLParser.SrsAttributeContext):
        pass


    # Enter a parse tree produced by SQLParser#dropStatement.
    def enterDropStatement(self, ctx:SQLParser.DropStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#dropStatement.
    def exitDropStatement(self, ctx:SQLParser.DropStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#dropDatabase.
    def enterDropDatabase(self, ctx:SQLParser.DropDatabaseContext):
        pass

    # Exit a parse tree produced by SQLParser#dropDatabase.
    def exitDropDatabase(self, ctx:SQLParser.DropDatabaseContext):
        pass


    # Enter a parse tree produced by SQLParser#dropEvent.
    def enterDropEvent(self, ctx:SQLParser.DropEventContext):
        pass

    # Exit a parse tree produced by SQLParser#dropEvent.
    def exitDropEvent(self, ctx:SQLParser.DropEventContext):
        pass


    # Enter a parse tree produced by SQLParser#dropFunction.
    def enterDropFunction(self, ctx:SQLParser.DropFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#dropFunction.
    def exitDropFunction(self, ctx:SQLParser.DropFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#dropProcedure.
    def enterDropProcedure(self, ctx:SQLParser.DropProcedureContext):
        pass

    # Exit a parse tree produced by SQLParser#dropProcedure.
    def exitDropProcedure(self, ctx:SQLParser.DropProcedureContext):
        pass


    # Enter a parse tree produced by SQLParser#dropIndex.
    def enterDropIndex(self, ctx:SQLParser.DropIndexContext):
        pass

    # Exit a parse tree produced by SQLParser#dropIndex.
    def exitDropIndex(self, ctx:SQLParser.DropIndexContext):
        pass


    # Enter a parse tree produced by SQLParser#dropLogfileGroup.
    def enterDropLogfileGroup(self, ctx:SQLParser.DropLogfileGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#dropLogfileGroup.
    def exitDropLogfileGroup(self, ctx:SQLParser.DropLogfileGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#dropLogfileGroupOption.
    def enterDropLogfileGroupOption(self, ctx:SQLParser.DropLogfileGroupOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#dropLogfileGroupOption.
    def exitDropLogfileGroupOption(self, ctx:SQLParser.DropLogfileGroupOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#dropServer.
    def enterDropServer(self, ctx:SQLParser.DropServerContext):
        pass

    # Exit a parse tree produced by SQLParser#dropServer.
    def exitDropServer(self, ctx:SQLParser.DropServerContext):
        pass


    # Enter a parse tree produced by SQLParser#dropTable.
    def enterDropTable(self, ctx:SQLParser.DropTableContext):
        pass

    # Exit a parse tree produced by SQLParser#dropTable.
    def exitDropTable(self, ctx:SQLParser.DropTableContext):
        pass


    # Enter a parse tree produced by SQLParser#dropTableSpace.
    def enterDropTableSpace(self, ctx:SQLParser.DropTableSpaceContext):
        pass

    # Exit a parse tree produced by SQLParser#dropTableSpace.
    def exitDropTableSpace(self, ctx:SQLParser.DropTableSpaceContext):
        pass


    # Enter a parse tree produced by SQLParser#dropTrigger.
    def enterDropTrigger(self, ctx:SQLParser.DropTriggerContext):
        pass

    # Exit a parse tree produced by SQLParser#dropTrigger.
    def exitDropTrigger(self, ctx:SQLParser.DropTriggerContext):
        pass


    # Enter a parse tree produced by SQLParser#dropView.
    def enterDropView(self, ctx:SQLParser.DropViewContext):
        pass

    # Exit a parse tree produced by SQLParser#dropView.
    def exitDropView(self, ctx:SQLParser.DropViewContext):
        pass


    # Enter a parse tree produced by SQLParser#dropRole.
    def enterDropRole(self, ctx:SQLParser.DropRoleContext):
        pass

    # Exit a parse tree produced by SQLParser#dropRole.
    def exitDropRole(self, ctx:SQLParser.DropRoleContext):
        pass


    # Enter a parse tree produced by SQLParser#dropSpatialReference.
    def enterDropSpatialReference(self, ctx:SQLParser.DropSpatialReferenceContext):
        pass

    # Exit a parse tree produced by SQLParser#dropSpatialReference.
    def exitDropSpatialReference(self, ctx:SQLParser.DropSpatialReferenceContext):
        pass


    # Enter a parse tree produced by SQLParser#dropUndoTablespace.
    def enterDropUndoTablespace(self, ctx:SQLParser.DropUndoTablespaceContext):
        pass

    # Exit a parse tree produced by SQLParser#dropUndoTablespace.
    def exitDropUndoTablespace(self, ctx:SQLParser.DropUndoTablespaceContext):
        pass


    # Enter a parse tree produced by SQLParser#renameTableStatement.
    def enterRenameTableStatement(self, ctx:SQLParser.RenameTableStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#renameTableStatement.
    def exitRenameTableStatement(self, ctx:SQLParser.RenameTableStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#renamePair.
    def enterRenamePair(self, ctx:SQLParser.RenamePairContext):
        pass

    # Exit a parse tree produced by SQLParser#renamePair.
    def exitRenamePair(self, ctx:SQLParser.RenamePairContext):
        pass


    # Enter a parse tree produced by SQLParser#truncateTableStatement.
    def enterTruncateTableStatement(self, ctx:SQLParser.TruncateTableStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#truncateTableStatement.
    def exitTruncateTableStatement(self, ctx:SQLParser.TruncateTableStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#importStatement.
    def enterImportStatement(self, ctx:SQLParser.ImportStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#importStatement.
    def exitImportStatement(self, ctx:SQLParser.ImportStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#callStatement.
    def enterCallStatement(self, ctx:SQLParser.CallStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#callStatement.
    def exitCallStatement(self, ctx:SQLParser.CallStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#deleteStatement.
    def enterDeleteStatement(self, ctx:SQLParser.DeleteStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#deleteStatement.
    def exitDeleteStatement(self, ctx:SQLParser.DeleteStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDelete.
    def enterPartitionDelete(self, ctx:SQLParser.PartitionDeleteContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDelete.
    def exitPartitionDelete(self, ctx:SQLParser.PartitionDeleteContext):
        pass


    # Enter a parse tree produced by SQLParser#deleteStatementOption.
    def enterDeleteStatementOption(self, ctx:SQLParser.DeleteStatementOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#deleteStatementOption.
    def exitDeleteStatementOption(self, ctx:SQLParser.DeleteStatementOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#doStatement.
    def enterDoStatement(self, ctx:SQLParser.DoStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#doStatement.
    def exitDoStatement(self, ctx:SQLParser.DoStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#handlerStatement.
    def enterHandlerStatement(self, ctx:SQLParser.HandlerStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#handlerStatement.
    def exitHandlerStatement(self, ctx:SQLParser.HandlerStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#handlerReadOrScan.
    def enterHandlerReadOrScan(self, ctx:SQLParser.HandlerReadOrScanContext):
        pass

    # Exit a parse tree produced by SQLParser#handlerReadOrScan.
    def exitHandlerReadOrScan(self, ctx:SQLParser.HandlerReadOrScanContext):
        pass


    # Enter a parse tree produced by SQLParser#insertStatement.
    def enterInsertStatement(self, ctx:SQLParser.InsertStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#insertStatement.
    def exitInsertStatement(self, ctx:SQLParser.InsertStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#insertLockOption.
    def enterInsertLockOption(self, ctx:SQLParser.InsertLockOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#insertLockOption.
    def exitInsertLockOption(self, ctx:SQLParser.InsertLockOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#insertFromConstructor.
    def enterInsertFromConstructor(self, ctx:SQLParser.InsertFromConstructorContext):
        pass

    # Exit a parse tree produced by SQLParser#insertFromConstructor.
    def exitInsertFromConstructor(self, ctx:SQLParser.InsertFromConstructorContext):
        pass


    # Enter a parse tree produced by SQLParser#fields.
    def enterFields(self, ctx:SQLParser.FieldsContext):
        pass

    # Exit a parse tree produced by SQLParser#fields.
    def exitFields(self, ctx:SQLParser.FieldsContext):
        pass


    # Enter a parse tree produced by SQLParser#insertValues.
    def enterInsertValues(self, ctx:SQLParser.InsertValuesContext):
        pass

    # Exit a parse tree produced by SQLParser#insertValues.
    def exitInsertValues(self, ctx:SQLParser.InsertValuesContext):
        pass


    # Enter a parse tree produced by SQLParser#insertQueryExpression.
    def enterInsertQueryExpression(self, ctx:SQLParser.InsertQueryExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#insertQueryExpression.
    def exitInsertQueryExpression(self, ctx:SQLParser.InsertQueryExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#valueList.
    def enterValueList(self, ctx:SQLParser.ValueListContext):
        pass

    # Exit a parse tree produced by SQLParser#valueList.
    def exitValueList(self, ctx:SQLParser.ValueListContext):
        pass


    # Enter a parse tree produced by SQLParser#values.
    def enterValues(self, ctx:SQLParser.ValuesContext):
        pass

    # Exit a parse tree produced by SQLParser#values.
    def exitValues(self, ctx:SQLParser.ValuesContext):
        pass


    # Enter a parse tree produced by SQLParser#valuesReference.
    def enterValuesReference(self, ctx:SQLParser.ValuesReferenceContext):
        pass

    # Exit a parse tree produced by SQLParser#valuesReference.
    def exitValuesReference(self, ctx:SQLParser.ValuesReferenceContext):
        pass


    # Enter a parse tree produced by SQLParser#insertUpdateList.
    def enterInsertUpdateList(self, ctx:SQLParser.InsertUpdateListContext):
        pass

    # Exit a parse tree produced by SQLParser#insertUpdateList.
    def exitInsertUpdateList(self, ctx:SQLParser.InsertUpdateListContext):
        pass


    # Enter a parse tree produced by SQLParser#loadStatement.
    def enterLoadStatement(self, ctx:SQLParser.LoadStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#loadStatement.
    def exitLoadStatement(self, ctx:SQLParser.LoadStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#dataOrXml.
    def enterDataOrXml(self, ctx:SQLParser.DataOrXmlContext):
        pass

    # Exit a parse tree produced by SQLParser#dataOrXml.
    def exitDataOrXml(self, ctx:SQLParser.DataOrXmlContext):
        pass


    # Enter a parse tree produced by SQLParser#xmlRowsIdentifiedBy.
    def enterXmlRowsIdentifiedBy(self, ctx:SQLParser.XmlRowsIdentifiedByContext):
        pass

    # Exit a parse tree produced by SQLParser#xmlRowsIdentifiedBy.
    def exitXmlRowsIdentifiedBy(self, ctx:SQLParser.XmlRowsIdentifiedByContext):
        pass


    # Enter a parse tree produced by SQLParser#loadDataFileTail.
    def enterLoadDataFileTail(self, ctx:SQLParser.LoadDataFileTailContext):
        pass

    # Exit a parse tree produced by SQLParser#loadDataFileTail.
    def exitLoadDataFileTail(self, ctx:SQLParser.LoadDataFileTailContext):
        pass


    # Enter a parse tree produced by SQLParser#loadDataFileTargetList.
    def enterLoadDataFileTargetList(self, ctx:SQLParser.LoadDataFileTargetListContext):
        pass

    # Exit a parse tree produced by SQLParser#loadDataFileTargetList.
    def exitLoadDataFileTargetList(self, ctx:SQLParser.LoadDataFileTargetListContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldOrVariableList.
    def enterFieldOrVariableList(self, ctx:SQLParser.FieldOrVariableListContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldOrVariableList.
    def exitFieldOrVariableList(self, ctx:SQLParser.FieldOrVariableListContext):
        pass


    # Enter a parse tree produced by SQLParser#replaceStatement.
    def enterReplaceStatement(self, ctx:SQLParser.ReplaceStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#replaceStatement.
    def exitReplaceStatement(self, ctx:SQLParser.ReplaceStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#selectStatement.
    def enterSelectStatement(self, ctx:SQLParser.SelectStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#selectStatement.
    def exitSelectStatement(self, ctx:SQLParser.SelectStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#selectStatementWithInto.
    def enterSelectStatementWithInto(self, ctx:SQLParser.SelectStatementWithIntoContext):
        pass

    # Exit a parse tree produced by SQLParser#selectStatementWithInto.
    def exitSelectStatementWithInto(self, ctx:SQLParser.SelectStatementWithIntoContext):
        pass


    # Enter a parse tree produced by SQLParser#queryExpression.
    def enterQueryExpression(self, ctx:SQLParser.QueryExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#queryExpression.
    def exitQueryExpression(self, ctx:SQLParser.QueryExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#queryExpressionBody.
    def enterQueryExpressionBody(self, ctx:SQLParser.QueryExpressionBodyContext):
        pass

    # Exit a parse tree produced by SQLParser#queryExpressionBody.
    def exitQueryExpressionBody(self, ctx:SQLParser.QueryExpressionBodyContext):
        pass


    # Enter a parse tree produced by SQLParser#queryExpressionParens.
    def enterQueryExpressionParens(self, ctx:SQLParser.QueryExpressionParensContext):
        pass

    # Exit a parse tree produced by SQLParser#queryExpressionParens.
    def exitQueryExpressionParens(self, ctx:SQLParser.QueryExpressionParensContext):
        pass


    # Enter a parse tree produced by SQLParser#queryPrimary.
    def enterQueryPrimary(self, ctx:SQLParser.QueryPrimaryContext):
        pass

    # Exit a parse tree produced by SQLParser#queryPrimary.
    def exitQueryPrimary(self, ctx:SQLParser.QueryPrimaryContext):
        pass


    # Enter a parse tree produced by SQLParser#querySpecification.
    def enterQuerySpecification(self, ctx:SQLParser.QuerySpecificationContext):
        pass

    # Exit a parse tree produced by SQLParser#querySpecification.
    def exitQuerySpecification(self, ctx:SQLParser.QuerySpecificationContext):
        pass


    # Enter a parse tree produced by SQLParser#subquery.
    def enterSubquery(self, ctx:SQLParser.SubqueryContext):
        pass

    # Exit a parse tree produced by SQLParser#subquery.
    def exitSubquery(self, ctx:SQLParser.SubqueryContext):
        pass


    # Enter a parse tree produced by SQLParser#querySpecOption.
    def enterQuerySpecOption(self, ctx:SQLParser.QuerySpecOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#querySpecOption.
    def exitQuerySpecOption(self, ctx:SQLParser.QuerySpecOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#limitClause.
    def enterLimitClause(self, ctx:SQLParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#limitClause.
    def exitLimitClause(self, ctx:SQLParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleLimitClause.
    def enterSimpleLimitClause(self, ctx:SQLParser.SimpleLimitClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleLimitClause.
    def exitSimpleLimitClause(self, ctx:SQLParser.SimpleLimitClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#limitOptions.
    def enterLimitOptions(self, ctx:SQLParser.LimitOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#limitOptions.
    def exitLimitOptions(self, ctx:SQLParser.LimitOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#limitOption.
    def enterLimitOption(self, ctx:SQLParser.LimitOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#limitOption.
    def exitLimitOption(self, ctx:SQLParser.LimitOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#intoClause.
    def enterIntoClause(self, ctx:SQLParser.IntoClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#intoClause.
    def exitIntoClause(self, ctx:SQLParser.IntoClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#procedureAnalyseClause.
    def enterProcedureAnalyseClause(self, ctx:SQLParser.ProcedureAnalyseClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#procedureAnalyseClause.
    def exitProcedureAnalyseClause(self, ctx:SQLParser.ProcedureAnalyseClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#havingClause.
    def enterHavingClause(self, ctx:SQLParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#havingClause.
    def exitHavingClause(self, ctx:SQLParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#windowClause.
    def enterWindowClause(self, ctx:SQLParser.WindowClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#windowClause.
    def exitWindowClause(self, ctx:SQLParser.WindowClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#windowDefinition.
    def enterWindowDefinition(self, ctx:SQLParser.WindowDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#windowDefinition.
    def exitWindowDefinition(self, ctx:SQLParser.WindowDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#windowSpec.
    def enterWindowSpec(self, ctx:SQLParser.WindowSpecContext):
        pass

    # Exit a parse tree produced by SQLParser#windowSpec.
    def exitWindowSpec(self, ctx:SQLParser.WindowSpecContext):
        pass


    # Enter a parse tree produced by SQLParser#windowSpecDetails.
    def enterWindowSpecDetails(self, ctx:SQLParser.WindowSpecDetailsContext):
        pass

    # Exit a parse tree produced by SQLParser#windowSpecDetails.
    def exitWindowSpecDetails(self, ctx:SQLParser.WindowSpecDetailsContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameClause.
    def enterWindowFrameClause(self, ctx:SQLParser.WindowFrameClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameClause.
    def exitWindowFrameClause(self, ctx:SQLParser.WindowFrameClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameUnits.
    def enterWindowFrameUnits(self, ctx:SQLParser.WindowFrameUnitsContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameUnits.
    def exitWindowFrameUnits(self, ctx:SQLParser.WindowFrameUnitsContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameExtent.
    def enterWindowFrameExtent(self, ctx:SQLParser.WindowFrameExtentContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameExtent.
    def exitWindowFrameExtent(self, ctx:SQLParser.WindowFrameExtentContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameStart.
    def enterWindowFrameStart(self, ctx:SQLParser.WindowFrameStartContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameStart.
    def exitWindowFrameStart(self, ctx:SQLParser.WindowFrameStartContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameBetween.
    def enterWindowFrameBetween(self, ctx:SQLParser.WindowFrameBetweenContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameBetween.
    def exitWindowFrameBetween(self, ctx:SQLParser.WindowFrameBetweenContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameBound.
    def enterWindowFrameBound(self, ctx:SQLParser.WindowFrameBoundContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameBound.
    def exitWindowFrameBound(self, ctx:SQLParser.WindowFrameBoundContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFrameExclusion.
    def enterWindowFrameExclusion(self, ctx:SQLParser.WindowFrameExclusionContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFrameExclusion.
    def exitWindowFrameExclusion(self, ctx:SQLParser.WindowFrameExclusionContext):
        pass


    # Enter a parse tree produced by SQLParser#withClause.
    def enterWithClause(self, ctx:SQLParser.WithClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#withClause.
    def exitWithClause(self, ctx:SQLParser.WithClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#commonTableExpression.
    def enterCommonTableExpression(self, ctx:SQLParser.CommonTableExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#commonTableExpression.
    def exitCommonTableExpression(self, ctx:SQLParser.CommonTableExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#groupByClause.
    def enterGroupByClause(self, ctx:SQLParser.GroupByClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#groupByClause.
    def exitGroupByClause(self, ctx:SQLParser.GroupByClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#olapOption.
    def enterOlapOption(self, ctx:SQLParser.OlapOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#olapOption.
    def exitOlapOption(self, ctx:SQLParser.OlapOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#orderClause.
    def enterOrderClause(self, ctx:SQLParser.OrderClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#orderClause.
    def exitOrderClause(self, ctx:SQLParser.OrderClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#direction.
    def enterDirection(self, ctx:SQLParser.DirectionContext):
        pass

    # Exit a parse tree produced by SQLParser#direction.
    def exitDirection(self, ctx:SQLParser.DirectionContext):
        pass


    # Enter a parse tree produced by SQLParser#fromClause.
    def enterFromClause(self, ctx:SQLParser.FromClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#fromClause.
    def exitFromClause(self, ctx:SQLParser.FromClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#tableReferenceList.
    def enterTableReferenceList(self, ctx:SQLParser.TableReferenceListContext):
        pass

    # Exit a parse tree produced by SQLParser#tableReferenceList.
    def exitTableReferenceList(self, ctx:SQLParser.TableReferenceListContext):
        pass


    # Enter a parse tree produced by SQLParser#tableValueConstructor.
    def enterTableValueConstructor(self, ctx:SQLParser.TableValueConstructorContext):
        pass

    # Exit a parse tree produced by SQLParser#tableValueConstructor.
    def exitTableValueConstructor(self, ctx:SQLParser.TableValueConstructorContext):
        pass


    # Enter a parse tree produced by SQLParser#explicitTable.
    def enterExplicitTable(self, ctx:SQLParser.ExplicitTableContext):
        pass

    # Exit a parse tree produced by SQLParser#explicitTable.
    def exitExplicitTable(self, ctx:SQLParser.ExplicitTableContext):
        pass


    # Enter a parse tree produced by SQLParser#rowValueExplicit.
    def enterRowValueExplicit(self, ctx:SQLParser.RowValueExplicitContext):
        pass

    # Exit a parse tree produced by SQLParser#rowValueExplicit.
    def exitRowValueExplicit(self, ctx:SQLParser.RowValueExplicitContext):
        pass


    # Enter a parse tree produced by SQLParser#selectOption.
    def enterSelectOption(self, ctx:SQLParser.SelectOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#selectOption.
    def exitSelectOption(self, ctx:SQLParser.SelectOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#lockingClauseList.
    def enterLockingClauseList(self, ctx:SQLParser.LockingClauseListContext):
        pass

    # Exit a parse tree produced by SQLParser#lockingClauseList.
    def exitLockingClauseList(self, ctx:SQLParser.LockingClauseListContext):
        pass


    # Enter a parse tree produced by SQLParser#lockingClause.
    def enterLockingClause(self, ctx:SQLParser.LockingClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#lockingClause.
    def exitLockingClause(self, ctx:SQLParser.LockingClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#lockStrengh.
    def enterLockStrengh(self, ctx:SQLParser.LockStrenghContext):
        pass

    # Exit a parse tree produced by SQLParser#lockStrengh.
    def exitLockStrengh(self, ctx:SQLParser.LockStrenghContext):
        pass


    # Enter a parse tree produced by SQLParser#lockedRowAction.
    def enterLockedRowAction(self, ctx:SQLParser.LockedRowActionContext):
        pass

    # Exit a parse tree produced by SQLParser#lockedRowAction.
    def exitLockedRowAction(self, ctx:SQLParser.LockedRowActionContext):
        pass


    # Enter a parse tree produced by SQLParser#selectItemList.
    def enterSelectItemList(self, ctx:SQLParser.SelectItemListContext):
        pass

    # Exit a parse tree produced by SQLParser#selectItemList.
    def exitSelectItemList(self, ctx:SQLParser.SelectItemListContext):
        pass


    # Enter a parse tree produced by SQLParser#selectItem.
    def enterSelectItem(self, ctx:SQLParser.SelectItemContext):
        pass

    # Exit a parse tree produced by SQLParser#selectItem.
    def exitSelectItem(self, ctx:SQLParser.SelectItemContext):
        pass


    # Enter a parse tree produced by SQLParser#selectAlias.
    def enterSelectAlias(self, ctx:SQLParser.SelectAliasContext):
        pass

    # Exit a parse tree produced by SQLParser#selectAlias.
    def exitSelectAlias(self, ctx:SQLParser.SelectAliasContext):
        pass


    # Enter a parse tree produced by SQLParser#whereClause.
    def enterWhereClause(self, ctx:SQLParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#whereClause.
    def exitWhereClause(self, ctx:SQLParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#tableReference.
    def enterTableReference(self, ctx:SQLParser.TableReferenceContext):
        pass

    # Exit a parse tree produced by SQLParser#tableReference.
    def exitTableReference(self, ctx:SQLParser.TableReferenceContext):
        pass


    # Enter a parse tree produced by SQLParser#escapedTableReference.
    def enterEscapedTableReference(self, ctx:SQLParser.EscapedTableReferenceContext):
        pass

    # Exit a parse tree produced by SQLParser#escapedTableReference.
    def exitEscapedTableReference(self, ctx:SQLParser.EscapedTableReferenceContext):
        pass


    # Enter a parse tree produced by SQLParser#joinedTable.
    def enterJoinedTable(self, ctx:SQLParser.JoinedTableContext):
        pass

    # Exit a parse tree produced by SQLParser#joinedTable.
    def exitJoinedTable(self, ctx:SQLParser.JoinedTableContext):
        pass


    # Enter a parse tree produced by SQLParser#naturalJoinType.
    def enterNaturalJoinType(self, ctx:SQLParser.NaturalJoinTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#naturalJoinType.
    def exitNaturalJoinType(self, ctx:SQLParser.NaturalJoinTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#innerJoinType.
    def enterInnerJoinType(self, ctx:SQLParser.InnerJoinTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#innerJoinType.
    def exitInnerJoinType(self, ctx:SQLParser.InnerJoinTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#outerJoinType.
    def enterOuterJoinType(self, ctx:SQLParser.OuterJoinTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#outerJoinType.
    def exitOuterJoinType(self, ctx:SQLParser.OuterJoinTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#tableFactor.
    def enterTableFactor(self, ctx:SQLParser.TableFactorContext):
        pass

    # Exit a parse tree produced by SQLParser#tableFactor.
    def exitTableFactor(self, ctx:SQLParser.TableFactorContext):
        pass


    # Enter a parse tree produced by SQLParser#singleTable.
    def enterSingleTable(self, ctx:SQLParser.SingleTableContext):
        pass

    # Exit a parse tree produced by SQLParser#singleTable.
    def exitSingleTable(self, ctx:SQLParser.SingleTableContext):
        pass


    # Enter a parse tree produced by SQLParser#singleTableParens.
    def enterSingleTableParens(self, ctx:SQLParser.SingleTableParensContext):
        pass

    # Exit a parse tree produced by SQLParser#singleTableParens.
    def exitSingleTableParens(self, ctx:SQLParser.SingleTableParensContext):
        pass


    # Enter a parse tree produced by SQLParser#derivedTable.
    def enterDerivedTable(self, ctx:SQLParser.DerivedTableContext):
        pass

    # Exit a parse tree produced by SQLParser#derivedTable.
    def exitDerivedTable(self, ctx:SQLParser.DerivedTableContext):
        pass


    # Enter a parse tree produced by SQLParser#tableReferenceListParens.
    def enterTableReferenceListParens(self, ctx:SQLParser.TableReferenceListParensContext):
        pass

    # Exit a parse tree produced by SQLParser#tableReferenceListParens.
    def exitTableReferenceListParens(self, ctx:SQLParser.TableReferenceListParensContext):
        pass


    # Enter a parse tree produced by SQLParser#tableFunction.
    def enterTableFunction(self, ctx:SQLParser.TableFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#tableFunction.
    def exitTableFunction(self, ctx:SQLParser.TableFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#columnsClause.
    def enterColumnsClause(self, ctx:SQLParser.ColumnsClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#columnsClause.
    def exitColumnsClause(self, ctx:SQLParser.ColumnsClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#jtColumn.
    def enterJtColumn(self, ctx:SQLParser.JtColumnContext):
        pass

    # Exit a parse tree produced by SQLParser#jtColumn.
    def exitJtColumn(self, ctx:SQLParser.JtColumnContext):
        pass


    # Enter a parse tree produced by SQLParser#onEmptyOrError.
    def enterOnEmptyOrError(self, ctx:SQLParser.OnEmptyOrErrorContext):
        pass

    # Exit a parse tree produced by SQLParser#onEmptyOrError.
    def exitOnEmptyOrError(self, ctx:SQLParser.OnEmptyOrErrorContext):
        pass


    # Enter a parse tree produced by SQLParser#onEmpty.
    def enterOnEmpty(self, ctx:SQLParser.OnEmptyContext):
        pass

    # Exit a parse tree produced by SQLParser#onEmpty.
    def exitOnEmpty(self, ctx:SQLParser.OnEmptyContext):
        pass


    # Enter a parse tree produced by SQLParser#onError.
    def enterOnError(self, ctx:SQLParser.OnErrorContext):
        pass

    # Exit a parse tree produced by SQLParser#onError.
    def exitOnError(self, ctx:SQLParser.OnErrorContext):
        pass


    # Enter a parse tree produced by SQLParser#jtOnResponse.
    def enterJtOnResponse(self, ctx:SQLParser.JtOnResponseContext):
        pass

    # Exit a parse tree produced by SQLParser#jtOnResponse.
    def exitJtOnResponse(self, ctx:SQLParser.JtOnResponseContext):
        pass


    # Enter a parse tree produced by SQLParser#unionOption.
    def enterUnionOption(self, ctx:SQLParser.UnionOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#unionOption.
    def exitUnionOption(self, ctx:SQLParser.UnionOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#tableAlias.
    def enterTableAlias(self, ctx:SQLParser.TableAliasContext):
        pass

    # Exit a parse tree produced by SQLParser#tableAlias.
    def exitTableAlias(self, ctx:SQLParser.TableAliasContext):
        pass


    # Enter a parse tree produced by SQLParser#indexHintList.
    def enterIndexHintList(self, ctx:SQLParser.IndexHintListContext):
        pass

    # Exit a parse tree produced by SQLParser#indexHintList.
    def exitIndexHintList(self, ctx:SQLParser.IndexHintListContext):
        pass


    # Enter a parse tree produced by SQLParser#indexHint.
    def enterIndexHint(self, ctx:SQLParser.IndexHintContext):
        pass

    # Exit a parse tree produced by SQLParser#indexHint.
    def exitIndexHint(self, ctx:SQLParser.IndexHintContext):
        pass


    # Enter a parse tree produced by SQLParser#indexHintType.
    def enterIndexHintType(self, ctx:SQLParser.IndexHintTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#indexHintType.
    def exitIndexHintType(self, ctx:SQLParser.IndexHintTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#keyOrIndex.
    def enterKeyOrIndex(self, ctx:SQLParser.KeyOrIndexContext):
        pass

    # Exit a parse tree produced by SQLParser#keyOrIndex.
    def exitKeyOrIndex(self, ctx:SQLParser.KeyOrIndexContext):
        pass


    # Enter a parse tree produced by SQLParser#constraintKeyType.
    def enterConstraintKeyType(self, ctx:SQLParser.ConstraintKeyTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#constraintKeyType.
    def exitConstraintKeyType(self, ctx:SQLParser.ConstraintKeyTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#indexHintClause.
    def enterIndexHintClause(self, ctx:SQLParser.IndexHintClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#indexHintClause.
    def exitIndexHintClause(self, ctx:SQLParser.IndexHintClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#indexList.
    def enterIndexList(self, ctx:SQLParser.IndexListContext):
        pass

    # Exit a parse tree produced by SQLParser#indexList.
    def exitIndexList(self, ctx:SQLParser.IndexListContext):
        pass


    # Enter a parse tree produced by SQLParser#indexListElement.
    def enterIndexListElement(self, ctx:SQLParser.IndexListElementContext):
        pass

    # Exit a parse tree produced by SQLParser#indexListElement.
    def exitIndexListElement(self, ctx:SQLParser.IndexListElementContext):
        pass


    # Enter a parse tree produced by SQLParser#updateStatement.
    def enterUpdateStatement(self, ctx:SQLParser.UpdateStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#updateStatement.
    def exitUpdateStatement(self, ctx:SQLParser.UpdateStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#transactionOrLockingStatement.
    def enterTransactionOrLockingStatement(self, ctx:SQLParser.TransactionOrLockingStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#transactionOrLockingStatement.
    def exitTransactionOrLockingStatement(self, ctx:SQLParser.TransactionOrLockingStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#transactionStatement.
    def enterTransactionStatement(self, ctx:SQLParser.TransactionStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#transactionStatement.
    def exitTransactionStatement(self, ctx:SQLParser.TransactionStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#beginWork.
    def enterBeginWork(self, ctx:SQLParser.BeginWorkContext):
        pass

    # Exit a parse tree produced by SQLParser#beginWork.
    def exitBeginWork(self, ctx:SQLParser.BeginWorkContext):
        pass


    # Enter a parse tree produced by SQLParser#transactionCharacteristic.
    def enterTransactionCharacteristic(self, ctx:SQLParser.TransactionCharacteristicContext):
        pass

    # Exit a parse tree produced by SQLParser#transactionCharacteristic.
    def exitTransactionCharacteristic(self, ctx:SQLParser.TransactionCharacteristicContext):
        pass


    # Enter a parse tree produced by SQLParser#savepointStatement.
    def enterSavepointStatement(self, ctx:SQLParser.SavepointStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#savepointStatement.
    def exitSavepointStatement(self, ctx:SQLParser.SavepointStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#lockStatement.
    def enterLockStatement(self, ctx:SQLParser.LockStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#lockStatement.
    def exitLockStatement(self, ctx:SQLParser.LockStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#lockItem.
    def enterLockItem(self, ctx:SQLParser.LockItemContext):
        pass

    # Exit a parse tree produced by SQLParser#lockItem.
    def exitLockItem(self, ctx:SQLParser.LockItemContext):
        pass


    # Enter a parse tree produced by SQLParser#lockOption.
    def enterLockOption(self, ctx:SQLParser.LockOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#lockOption.
    def exitLockOption(self, ctx:SQLParser.LockOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#xaStatement.
    def enterXaStatement(self, ctx:SQLParser.XaStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#xaStatement.
    def exitXaStatement(self, ctx:SQLParser.XaStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#xaConvert.
    def enterXaConvert(self, ctx:SQLParser.XaConvertContext):
        pass

    # Exit a parse tree produced by SQLParser#xaConvert.
    def exitXaConvert(self, ctx:SQLParser.XaConvertContext):
        pass


    # Enter a parse tree produced by SQLParser#xid.
    def enterXid(self, ctx:SQLParser.XidContext):
        pass

    # Exit a parse tree produced by SQLParser#xid.
    def exitXid(self, ctx:SQLParser.XidContext):
        pass


    # Enter a parse tree produced by SQLParser#replicationStatement.
    def enterReplicationStatement(self, ctx:SQLParser.ReplicationStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#replicationStatement.
    def exitReplicationStatement(self, ctx:SQLParser.ReplicationStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#resetOption.
    def enterResetOption(self, ctx:SQLParser.ResetOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#resetOption.
    def exitResetOption(self, ctx:SQLParser.ResetOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#masterResetOptions.
    def enterMasterResetOptions(self, ctx:SQLParser.MasterResetOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#masterResetOptions.
    def exitMasterResetOptions(self, ctx:SQLParser.MasterResetOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#replicationLoad.
    def enterReplicationLoad(self, ctx:SQLParser.ReplicationLoadContext):
        pass

    # Exit a parse tree produced by SQLParser#replicationLoad.
    def exitReplicationLoad(self, ctx:SQLParser.ReplicationLoadContext):
        pass


    # Enter a parse tree produced by SQLParser#changeMaster.
    def enterChangeMaster(self, ctx:SQLParser.ChangeMasterContext):
        pass

    # Exit a parse tree produced by SQLParser#changeMaster.
    def exitChangeMaster(self, ctx:SQLParser.ChangeMasterContext):
        pass


    # Enter a parse tree produced by SQLParser#changeMasterOptions.
    def enterChangeMasterOptions(self, ctx:SQLParser.ChangeMasterOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#changeMasterOptions.
    def exitChangeMasterOptions(self, ctx:SQLParser.ChangeMasterOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#masterOption.
    def enterMasterOption(self, ctx:SQLParser.MasterOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#masterOption.
    def exitMasterOption(self, ctx:SQLParser.MasterOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#privilegeCheckDef.
    def enterPrivilegeCheckDef(self, ctx:SQLParser.PrivilegeCheckDefContext):
        pass

    # Exit a parse tree produced by SQLParser#privilegeCheckDef.
    def exitPrivilegeCheckDef(self, ctx:SQLParser.PrivilegeCheckDefContext):
        pass


    # Enter a parse tree produced by SQLParser#tablePrimaryKeyCheckDef.
    def enterTablePrimaryKeyCheckDef(self, ctx:SQLParser.TablePrimaryKeyCheckDefContext):
        pass

    # Exit a parse tree produced by SQLParser#tablePrimaryKeyCheckDef.
    def exitTablePrimaryKeyCheckDef(self, ctx:SQLParser.TablePrimaryKeyCheckDefContext):
        pass


    # Enter a parse tree produced by SQLParser#masterTlsCiphersuitesDef.
    def enterMasterTlsCiphersuitesDef(self, ctx:SQLParser.MasterTlsCiphersuitesDefContext):
        pass

    # Exit a parse tree produced by SQLParser#masterTlsCiphersuitesDef.
    def exitMasterTlsCiphersuitesDef(self, ctx:SQLParser.MasterTlsCiphersuitesDefContext):
        pass


    # Enter a parse tree produced by SQLParser#masterFileDef.
    def enterMasterFileDef(self, ctx:SQLParser.MasterFileDefContext):
        pass

    # Exit a parse tree produced by SQLParser#masterFileDef.
    def exitMasterFileDef(self, ctx:SQLParser.MasterFileDefContext):
        pass


    # Enter a parse tree produced by SQLParser#serverIdList.
    def enterServerIdList(self, ctx:SQLParser.ServerIdListContext):
        pass

    # Exit a parse tree produced by SQLParser#serverIdList.
    def exitServerIdList(self, ctx:SQLParser.ServerIdListContext):
        pass


    # Enter a parse tree produced by SQLParser#changeReplication.
    def enterChangeReplication(self, ctx:SQLParser.ChangeReplicationContext):
        pass

    # Exit a parse tree produced by SQLParser#changeReplication.
    def exitChangeReplication(self, ctx:SQLParser.ChangeReplicationContext):
        pass


    # Enter a parse tree produced by SQLParser#filterDefinition.
    def enterFilterDefinition(self, ctx:SQLParser.FilterDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#filterDefinition.
    def exitFilterDefinition(self, ctx:SQLParser.FilterDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#filterDbList.
    def enterFilterDbList(self, ctx:SQLParser.FilterDbListContext):
        pass

    # Exit a parse tree produced by SQLParser#filterDbList.
    def exitFilterDbList(self, ctx:SQLParser.FilterDbListContext):
        pass


    # Enter a parse tree produced by SQLParser#filterTableList.
    def enterFilterTableList(self, ctx:SQLParser.FilterTableListContext):
        pass

    # Exit a parse tree produced by SQLParser#filterTableList.
    def exitFilterTableList(self, ctx:SQLParser.FilterTableListContext):
        pass


    # Enter a parse tree produced by SQLParser#filterStringList.
    def enterFilterStringList(self, ctx:SQLParser.FilterStringListContext):
        pass

    # Exit a parse tree produced by SQLParser#filterStringList.
    def exitFilterStringList(self, ctx:SQLParser.FilterStringListContext):
        pass


    # Enter a parse tree produced by SQLParser#filterWildDbTableString.
    def enterFilterWildDbTableString(self, ctx:SQLParser.FilterWildDbTableStringContext):
        pass

    # Exit a parse tree produced by SQLParser#filterWildDbTableString.
    def exitFilterWildDbTableString(self, ctx:SQLParser.FilterWildDbTableStringContext):
        pass


    # Enter a parse tree produced by SQLParser#filterDbPairList.
    def enterFilterDbPairList(self, ctx:SQLParser.FilterDbPairListContext):
        pass

    # Exit a parse tree produced by SQLParser#filterDbPairList.
    def exitFilterDbPairList(self, ctx:SQLParser.FilterDbPairListContext):
        pass


    # Enter a parse tree produced by SQLParser#slave.
    def enterSlave(self, ctx:SQLParser.SlaveContext):
        pass

    # Exit a parse tree produced by SQLParser#slave.
    def exitSlave(self, ctx:SQLParser.SlaveContext):
        pass


    # Enter a parse tree produced by SQLParser#slaveUntilOptions.
    def enterSlaveUntilOptions(self, ctx:SQLParser.SlaveUntilOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#slaveUntilOptions.
    def exitSlaveUntilOptions(self, ctx:SQLParser.SlaveUntilOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#slaveConnectionOptions.
    def enterSlaveConnectionOptions(self, ctx:SQLParser.SlaveConnectionOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#slaveConnectionOptions.
    def exitSlaveConnectionOptions(self, ctx:SQLParser.SlaveConnectionOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#slaveThreadOptions.
    def enterSlaveThreadOptions(self, ctx:SQLParser.SlaveThreadOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#slaveThreadOptions.
    def exitSlaveThreadOptions(self, ctx:SQLParser.SlaveThreadOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#slaveThreadOption.
    def enterSlaveThreadOption(self, ctx:SQLParser.SlaveThreadOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#slaveThreadOption.
    def exitSlaveThreadOption(self, ctx:SQLParser.SlaveThreadOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#groupReplication.
    def enterGroupReplication(self, ctx:SQLParser.GroupReplicationContext):
        pass

    # Exit a parse tree produced by SQLParser#groupReplication.
    def exitGroupReplication(self, ctx:SQLParser.GroupReplicationContext):
        pass


    # Enter a parse tree produced by SQLParser#preparedStatement.
    def enterPreparedStatement(self, ctx:SQLParser.PreparedStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#preparedStatement.
    def exitPreparedStatement(self, ctx:SQLParser.PreparedStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#executeStatement.
    def enterExecuteStatement(self, ctx:SQLParser.ExecuteStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#executeStatement.
    def exitExecuteStatement(self, ctx:SQLParser.ExecuteStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#executeVarList.
    def enterExecuteVarList(self, ctx:SQLParser.ExecuteVarListContext):
        pass

    # Exit a parse tree produced by SQLParser#executeVarList.
    def exitExecuteVarList(self, ctx:SQLParser.ExecuteVarListContext):
        pass


    # Enter a parse tree produced by SQLParser#cloneStatement.
    def enterCloneStatement(self, ctx:SQLParser.CloneStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#cloneStatement.
    def exitCloneStatement(self, ctx:SQLParser.CloneStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#dataDirSSL.
    def enterDataDirSSL(self, ctx:SQLParser.DataDirSSLContext):
        pass

    # Exit a parse tree produced by SQLParser#dataDirSSL.
    def exitDataDirSSL(self, ctx:SQLParser.DataDirSSLContext):
        pass


    # Enter a parse tree produced by SQLParser#ssl.
    def enterSsl(self, ctx:SQLParser.SslContext):
        pass

    # Exit a parse tree produced by SQLParser#ssl.
    def exitSsl(self, ctx:SQLParser.SslContext):
        pass


    # Enter a parse tree produced by SQLParser#accountManagementStatement.
    def enterAccountManagementStatement(self, ctx:SQLParser.AccountManagementStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#accountManagementStatement.
    def exitAccountManagementStatement(self, ctx:SQLParser.AccountManagementStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#alterUser.
    def enterAlterUser(self, ctx:SQLParser.AlterUserContext):
        pass

    # Exit a parse tree produced by SQLParser#alterUser.
    def exitAlterUser(self, ctx:SQLParser.AlterUserContext):
        pass


    # Enter a parse tree produced by SQLParser#alterUserTail.
    def enterAlterUserTail(self, ctx:SQLParser.AlterUserTailContext):
        pass

    # Exit a parse tree produced by SQLParser#alterUserTail.
    def exitAlterUserTail(self, ctx:SQLParser.AlterUserTailContext):
        pass


    # Enter a parse tree produced by SQLParser#userFunction.
    def enterUserFunction(self, ctx:SQLParser.UserFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#userFunction.
    def exitUserFunction(self, ctx:SQLParser.UserFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#createUser.
    def enterCreateUser(self, ctx:SQLParser.CreateUserContext):
        pass

    # Exit a parse tree produced by SQLParser#createUser.
    def exitCreateUser(self, ctx:SQLParser.CreateUserContext):
        pass


    # Enter a parse tree produced by SQLParser#createUserTail.
    def enterCreateUserTail(self, ctx:SQLParser.CreateUserTailContext):
        pass

    # Exit a parse tree produced by SQLParser#createUserTail.
    def exitCreateUserTail(self, ctx:SQLParser.CreateUserTailContext):
        pass


    # Enter a parse tree produced by SQLParser#defaultRoleClause.
    def enterDefaultRoleClause(self, ctx:SQLParser.DefaultRoleClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#defaultRoleClause.
    def exitDefaultRoleClause(self, ctx:SQLParser.DefaultRoleClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#requireClause.
    def enterRequireClause(self, ctx:SQLParser.RequireClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#requireClause.
    def exitRequireClause(self, ctx:SQLParser.RequireClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#connectOptions.
    def enterConnectOptions(self, ctx:SQLParser.ConnectOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#connectOptions.
    def exitConnectOptions(self, ctx:SQLParser.ConnectOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#accountLockPasswordExpireOptions.
    def enterAccountLockPasswordExpireOptions(self, ctx:SQLParser.AccountLockPasswordExpireOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#accountLockPasswordExpireOptions.
    def exitAccountLockPasswordExpireOptions(self, ctx:SQLParser.AccountLockPasswordExpireOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#dropUser.
    def enterDropUser(self, ctx:SQLParser.DropUserContext):
        pass

    # Exit a parse tree produced by SQLParser#dropUser.
    def exitDropUser(self, ctx:SQLParser.DropUserContext):
        pass


    # Enter a parse tree produced by SQLParser#grant.
    def enterGrant(self, ctx:SQLParser.GrantContext):
        pass

    # Exit a parse tree produced by SQLParser#grant.
    def exitGrant(self, ctx:SQLParser.GrantContext):
        pass


    # Enter a parse tree produced by SQLParser#grantTargetList.
    def enterGrantTargetList(self, ctx:SQLParser.GrantTargetListContext):
        pass

    # Exit a parse tree produced by SQLParser#grantTargetList.
    def exitGrantTargetList(self, ctx:SQLParser.GrantTargetListContext):
        pass


    # Enter a parse tree produced by SQLParser#grantOptions.
    def enterGrantOptions(self, ctx:SQLParser.GrantOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#grantOptions.
    def exitGrantOptions(self, ctx:SQLParser.GrantOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#exceptRoleList.
    def enterExceptRoleList(self, ctx:SQLParser.ExceptRoleListContext):
        pass

    # Exit a parse tree produced by SQLParser#exceptRoleList.
    def exitExceptRoleList(self, ctx:SQLParser.ExceptRoleListContext):
        pass


    # Enter a parse tree produced by SQLParser#withRoles.
    def enterWithRoles(self, ctx:SQLParser.WithRolesContext):
        pass

    # Exit a parse tree produced by SQLParser#withRoles.
    def exitWithRoles(self, ctx:SQLParser.WithRolesContext):
        pass


    # Enter a parse tree produced by SQLParser#grantAs.
    def enterGrantAs(self, ctx:SQLParser.GrantAsContext):
        pass

    # Exit a parse tree produced by SQLParser#grantAs.
    def exitGrantAs(self, ctx:SQLParser.GrantAsContext):
        pass


    # Enter a parse tree produced by SQLParser#versionedRequireClause.
    def enterVersionedRequireClause(self, ctx:SQLParser.VersionedRequireClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#versionedRequireClause.
    def exitVersionedRequireClause(self, ctx:SQLParser.VersionedRequireClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#renameUser.
    def enterRenameUser(self, ctx:SQLParser.RenameUserContext):
        pass

    # Exit a parse tree produced by SQLParser#renameUser.
    def exitRenameUser(self, ctx:SQLParser.RenameUserContext):
        pass


    # Enter a parse tree produced by SQLParser#revoke.
    def enterRevoke(self, ctx:SQLParser.RevokeContext):
        pass

    # Exit a parse tree produced by SQLParser#revoke.
    def exitRevoke(self, ctx:SQLParser.RevokeContext):
        pass


    # Enter a parse tree produced by SQLParser#onTypeTo.
    def enterOnTypeTo(self, ctx:SQLParser.OnTypeToContext):
        pass

    # Exit a parse tree produced by SQLParser#onTypeTo.
    def exitOnTypeTo(self, ctx:SQLParser.OnTypeToContext):
        pass


    # Enter a parse tree produced by SQLParser#aclType.
    def enterAclType(self, ctx:SQLParser.AclTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#aclType.
    def exitAclType(self, ctx:SQLParser.AclTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#roleOrPrivilegesList.
    def enterRoleOrPrivilegesList(self, ctx:SQLParser.RoleOrPrivilegesListContext):
        pass

    # Exit a parse tree produced by SQLParser#roleOrPrivilegesList.
    def exitRoleOrPrivilegesList(self, ctx:SQLParser.RoleOrPrivilegesListContext):
        pass


    # Enter a parse tree produced by SQLParser#roleOrPrivilege.
    def enterRoleOrPrivilege(self, ctx:SQLParser.RoleOrPrivilegeContext):
        pass

    # Exit a parse tree produced by SQLParser#roleOrPrivilege.
    def exitRoleOrPrivilege(self, ctx:SQLParser.RoleOrPrivilegeContext):
        pass


    # Enter a parse tree produced by SQLParser#grantIdentifier.
    def enterGrantIdentifier(self, ctx:SQLParser.GrantIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#grantIdentifier.
    def exitGrantIdentifier(self, ctx:SQLParser.GrantIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#requireList.
    def enterRequireList(self, ctx:SQLParser.RequireListContext):
        pass

    # Exit a parse tree produced by SQLParser#requireList.
    def exitRequireList(self, ctx:SQLParser.RequireListContext):
        pass


    # Enter a parse tree produced by SQLParser#requireListElement.
    def enterRequireListElement(self, ctx:SQLParser.RequireListElementContext):
        pass

    # Exit a parse tree produced by SQLParser#requireListElement.
    def exitRequireListElement(self, ctx:SQLParser.RequireListElementContext):
        pass


    # Enter a parse tree produced by SQLParser#grantOption.
    def enterGrantOption(self, ctx:SQLParser.GrantOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#grantOption.
    def exitGrantOption(self, ctx:SQLParser.GrantOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#setRole.
    def enterSetRole(self, ctx:SQLParser.SetRoleContext):
        pass

    # Exit a parse tree produced by SQLParser#setRole.
    def exitSetRole(self, ctx:SQLParser.SetRoleContext):
        pass


    # Enter a parse tree produced by SQLParser#roleList.
    def enterRoleList(self, ctx:SQLParser.RoleListContext):
        pass

    # Exit a parse tree produced by SQLParser#roleList.
    def exitRoleList(self, ctx:SQLParser.RoleListContext):
        pass


    # Enter a parse tree produced by SQLParser#role.
    def enterRole(self, ctx:SQLParser.RoleContext):
        pass

    # Exit a parse tree produced by SQLParser#role.
    def exitRole(self, ctx:SQLParser.RoleContext):
        pass


    # Enter a parse tree produced by SQLParser#tableAdministrationStatement.
    def enterTableAdministrationStatement(self, ctx:SQLParser.TableAdministrationStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#tableAdministrationStatement.
    def exitTableAdministrationStatement(self, ctx:SQLParser.TableAdministrationStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#histogram.
    def enterHistogram(self, ctx:SQLParser.HistogramContext):
        pass

    # Exit a parse tree produced by SQLParser#histogram.
    def exitHistogram(self, ctx:SQLParser.HistogramContext):
        pass


    # Enter a parse tree produced by SQLParser#checkOption.
    def enterCheckOption(self, ctx:SQLParser.CheckOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#checkOption.
    def exitCheckOption(self, ctx:SQLParser.CheckOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#repairType.
    def enterRepairType(self, ctx:SQLParser.RepairTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#repairType.
    def exitRepairType(self, ctx:SQLParser.RepairTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#installUninstallStatment.
    def enterInstallUninstallStatment(self, ctx:SQLParser.InstallUninstallStatmentContext):
        pass

    # Exit a parse tree produced by SQLParser#installUninstallStatment.
    def exitInstallUninstallStatment(self, ctx:SQLParser.InstallUninstallStatmentContext):
        pass


    # Enter a parse tree produced by SQLParser#setStatement.
    def enterSetStatement(self, ctx:SQLParser.SetStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#setStatement.
    def exitSetStatement(self, ctx:SQLParser.SetStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#startOptionValueList.
    def enterStartOptionValueList(self, ctx:SQLParser.StartOptionValueListContext):
        pass

    # Exit a parse tree produced by SQLParser#startOptionValueList.
    def exitStartOptionValueList(self, ctx:SQLParser.StartOptionValueListContext):
        pass


    # Enter a parse tree produced by SQLParser#transactionCharacteristics.
    def enterTransactionCharacteristics(self, ctx:SQLParser.TransactionCharacteristicsContext):
        pass

    # Exit a parse tree produced by SQLParser#transactionCharacteristics.
    def exitTransactionCharacteristics(self, ctx:SQLParser.TransactionCharacteristicsContext):
        pass


    # Enter a parse tree produced by SQLParser#transactionAccessMode.
    def enterTransactionAccessMode(self, ctx:SQLParser.TransactionAccessModeContext):
        pass

    # Exit a parse tree produced by SQLParser#transactionAccessMode.
    def exitTransactionAccessMode(self, ctx:SQLParser.TransactionAccessModeContext):
        pass


    # Enter a parse tree produced by SQLParser#isolationLevel.
    def enterIsolationLevel(self, ctx:SQLParser.IsolationLevelContext):
        pass

    # Exit a parse tree produced by SQLParser#isolationLevel.
    def exitIsolationLevel(self, ctx:SQLParser.IsolationLevelContext):
        pass


    # Enter a parse tree produced by SQLParser#optionValueListContinued.
    def enterOptionValueListContinued(self, ctx:SQLParser.OptionValueListContinuedContext):
        pass

    # Exit a parse tree produced by SQLParser#optionValueListContinued.
    def exitOptionValueListContinued(self, ctx:SQLParser.OptionValueListContinuedContext):
        pass


    # Enter a parse tree produced by SQLParser#optionValueNoOptionType.
    def enterOptionValueNoOptionType(self, ctx:SQLParser.OptionValueNoOptionTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#optionValueNoOptionType.
    def exitOptionValueNoOptionType(self, ctx:SQLParser.OptionValueNoOptionTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#optionValue.
    def enterOptionValue(self, ctx:SQLParser.OptionValueContext):
        pass

    # Exit a parse tree produced by SQLParser#optionValue.
    def exitOptionValue(self, ctx:SQLParser.OptionValueContext):
        pass


    # Enter a parse tree produced by SQLParser#setSystemVariable.
    def enterSetSystemVariable(self, ctx:SQLParser.SetSystemVariableContext):
        pass

    # Exit a parse tree produced by SQLParser#setSystemVariable.
    def exitSetSystemVariable(self, ctx:SQLParser.SetSystemVariableContext):
        pass


    # Enter a parse tree produced by SQLParser#startOptionValueListFollowingOptionType.
    def enterStartOptionValueListFollowingOptionType(self, ctx:SQLParser.StartOptionValueListFollowingOptionTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#startOptionValueListFollowingOptionType.
    def exitStartOptionValueListFollowingOptionType(self, ctx:SQLParser.StartOptionValueListFollowingOptionTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#optionValueFollowingOptionType.
    def enterOptionValueFollowingOptionType(self, ctx:SQLParser.OptionValueFollowingOptionTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#optionValueFollowingOptionType.
    def exitOptionValueFollowingOptionType(self, ctx:SQLParser.OptionValueFollowingOptionTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#setExprOrDefault.
    def enterSetExprOrDefault(self, ctx:SQLParser.SetExprOrDefaultContext):
        pass

    # Exit a parse tree produced by SQLParser#setExprOrDefault.
    def exitSetExprOrDefault(self, ctx:SQLParser.SetExprOrDefaultContext):
        pass


    # Enter a parse tree produced by SQLParser#showStatement.
    def enterShowStatement(self, ctx:SQLParser.ShowStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#showStatement.
    def exitShowStatement(self, ctx:SQLParser.ShowStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#showCommandType.
    def enterShowCommandType(self, ctx:SQLParser.ShowCommandTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#showCommandType.
    def exitShowCommandType(self, ctx:SQLParser.ShowCommandTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#nonBlocking.
    def enterNonBlocking(self, ctx:SQLParser.NonBlockingContext):
        pass

    # Exit a parse tree produced by SQLParser#nonBlocking.
    def exitNonBlocking(self, ctx:SQLParser.NonBlockingContext):
        pass


    # Enter a parse tree produced by SQLParser#fromOrIn.
    def enterFromOrIn(self, ctx:SQLParser.FromOrInContext):
        pass

    # Exit a parse tree produced by SQLParser#fromOrIn.
    def exitFromOrIn(self, ctx:SQLParser.FromOrInContext):
        pass


    # Enter a parse tree produced by SQLParser#inDb.
    def enterInDb(self, ctx:SQLParser.InDbContext):
        pass

    # Exit a parse tree produced by SQLParser#inDb.
    def exitInDb(self, ctx:SQLParser.InDbContext):
        pass


    # Enter a parse tree produced by SQLParser#profileType.
    def enterProfileType(self, ctx:SQLParser.ProfileTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#profileType.
    def exitProfileType(self, ctx:SQLParser.ProfileTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#otherAdministrativeStatement.
    def enterOtherAdministrativeStatement(self, ctx:SQLParser.OtherAdministrativeStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#otherAdministrativeStatement.
    def exitOtherAdministrativeStatement(self, ctx:SQLParser.OtherAdministrativeStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#keyCacheListOrParts.
    def enterKeyCacheListOrParts(self, ctx:SQLParser.KeyCacheListOrPartsContext):
        pass

    # Exit a parse tree produced by SQLParser#keyCacheListOrParts.
    def exitKeyCacheListOrParts(self, ctx:SQLParser.KeyCacheListOrPartsContext):
        pass


    # Enter a parse tree produced by SQLParser#keyCacheList.
    def enterKeyCacheList(self, ctx:SQLParser.KeyCacheListContext):
        pass

    # Exit a parse tree produced by SQLParser#keyCacheList.
    def exitKeyCacheList(self, ctx:SQLParser.KeyCacheListContext):
        pass


    # Enter a parse tree produced by SQLParser#assignToKeycache.
    def enterAssignToKeycache(self, ctx:SQLParser.AssignToKeycacheContext):
        pass

    # Exit a parse tree produced by SQLParser#assignToKeycache.
    def exitAssignToKeycache(self, ctx:SQLParser.AssignToKeycacheContext):
        pass


    # Enter a parse tree produced by SQLParser#assignToKeycachePartition.
    def enterAssignToKeycachePartition(self, ctx:SQLParser.AssignToKeycachePartitionContext):
        pass

    # Exit a parse tree produced by SQLParser#assignToKeycachePartition.
    def exitAssignToKeycachePartition(self, ctx:SQLParser.AssignToKeycachePartitionContext):
        pass


    # Enter a parse tree produced by SQLParser#cacheKeyList.
    def enterCacheKeyList(self, ctx:SQLParser.CacheKeyListContext):
        pass

    # Exit a parse tree produced by SQLParser#cacheKeyList.
    def exitCacheKeyList(self, ctx:SQLParser.CacheKeyListContext):
        pass


    # Enter a parse tree produced by SQLParser#keyUsageElement.
    def enterKeyUsageElement(self, ctx:SQLParser.KeyUsageElementContext):
        pass

    # Exit a parse tree produced by SQLParser#keyUsageElement.
    def exitKeyUsageElement(self, ctx:SQLParser.KeyUsageElementContext):
        pass


    # Enter a parse tree produced by SQLParser#keyUsageList.
    def enterKeyUsageList(self, ctx:SQLParser.KeyUsageListContext):
        pass

    # Exit a parse tree produced by SQLParser#keyUsageList.
    def exitKeyUsageList(self, ctx:SQLParser.KeyUsageListContext):
        pass


    # Enter a parse tree produced by SQLParser#flushOption.
    def enterFlushOption(self, ctx:SQLParser.FlushOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#flushOption.
    def exitFlushOption(self, ctx:SQLParser.FlushOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#logType.
    def enterLogType(self, ctx:SQLParser.LogTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#logType.
    def exitLogType(self, ctx:SQLParser.LogTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#flushTables.
    def enterFlushTables(self, ctx:SQLParser.FlushTablesContext):
        pass

    # Exit a parse tree produced by SQLParser#flushTables.
    def exitFlushTables(self, ctx:SQLParser.FlushTablesContext):
        pass


    # Enter a parse tree produced by SQLParser#flushTablesOptions.
    def enterFlushTablesOptions(self, ctx:SQLParser.FlushTablesOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#flushTablesOptions.
    def exitFlushTablesOptions(self, ctx:SQLParser.FlushTablesOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#preloadTail.
    def enterPreloadTail(self, ctx:SQLParser.PreloadTailContext):
        pass

    # Exit a parse tree produced by SQLParser#preloadTail.
    def exitPreloadTail(self, ctx:SQLParser.PreloadTailContext):
        pass


    # Enter a parse tree produced by SQLParser#preloadList.
    def enterPreloadList(self, ctx:SQLParser.PreloadListContext):
        pass

    # Exit a parse tree produced by SQLParser#preloadList.
    def exitPreloadList(self, ctx:SQLParser.PreloadListContext):
        pass


    # Enter a parse tree produced by SQLParser#preloadKeys.
    def enterPreloadKeys(self, ctx:SQLParser.PreloadKeysContext):
        pass

    # Exit a parse tree produced by SQLParser#preloadKeys.
    def exitPreloadKeys(self, ctx:SQLParser.PreloadKeysContext):
        pass


    # Enter a parse tree produced by SQLParser#adminPartition.
    def enterAdminPartition(self, ctx:SQLParser.AdminPartitionContext):
        pass

    # Exit a parse tree produced by SQLParser#adminPartition.
    def exitAdminPartition(self, ctx:SQLParser.AdminPartitionContext):
        pass


    # Enter a parse tree produced by SQLParser#resourceGroupManagement.
    def enterResourceGroupManagement(self, ctx:SQLParser.ResourceGroupManagementContext):
        pass

    # Exit a parse tree produced by SQLParser#resourceGroupManagement.
    def exitResourceGroupManagement(self, ctx:SQLParser.ResourceGroupManagementContext):
        pass


    # Enter a parse tree produced by SQLParser#createResourceGroup.
    def enterCreateResourceGroup(self, ctx:SQLParser.CreateResourceGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#createResourceGroup.
    def exitCreateResourceGroup(self, ctx:SQLParser.CreateResourceGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#resourceGroupVcpuList.
    def enterResourceGroupVcpuList(self, ctx:SQLParser.ResourceGroupVcpuListContext):
        pass

    # Exit a parse tree produced by SQLParser#resourceGroupVcpuList.
    def exitResourceGroupVcpuList(self, ctx:SQLParser.ResourceGroupVcpuListContext):
        pass


    # Enter a parse tree produced by SQLParser#vcpuNumOrRange.
    def enterVcpuNumOrRange(self, ctx:SQLParser.VcpuNumOrRangeContext):
        pass

    # Exit a parse tree produced by SQLParser#vcpuNumOrRange.
    def exitVcpuNumOrRange(self, ctx:SQLParser.VcpuNumOrRangeContext):
        pass


    # Enter a parse tree produced by SQLParser#resourceGroupPriority.
    def enterResourceGroupPriority(self, ctx:SQLParser.ResourceGroupPriorityContext):
        pass

    # Exit a parse tree produced by SQLParser#resourceGroupPriority.
    def exitResourceGroupPriority(self, ctx:SQLParser.ResourceGroupPriorityContext):
        pass


    # Enter a parse tree produced by SQLParser#resourceGroupEnableDisable.
    def enterResourceGroupEnableDisable(self, ctx:SQLParser.ResourceGroupEnableDisableContext):
        pass

    # Exit a parse tree produced by SQLParser#resourceGroupEnableDisable.
    def exitResourceGroupEnableDisable(self, ctx:SQLParser.ResourceGroupEnableDisableContext):
        pass


    # Enter a parse tree produced by SQLParser#alterResourceGroup.
    def enterAlterResourceGroup(self, ctx:SQLParser.AlterResourceGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#alterResourceGroup.
    def exitAlterResourceGroup(self, ctx:SQLParser.AlterResourceGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#setResourceGroup.
    def enterSetResourceGroup(self, ctx:SQLParser.SetResourceGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#setResourceGroup.
    def exitSetResourceGroup(self, ctx:SQLParser.SetResourceGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#threadIdList.
    def enterThreadIdList(self, ctx:SQLParser.ThreadIdListContext):
        pass

    # Exit a parse tree produced by SQLParser#threadIdList.
    def exitThreadIdList(self, ctx:SQLParser.ThreadIdListContext):
        pass


    # Enter a parse tree produced by SQLParser#dropResourceGroup.
    def enterDropResourceGroup(self, ctx:SQLParser.DropResourceGroupContext):
        pass

    # Exit a parse tree produced by SQLParser#dropResourceGroup.
    def exitDropResourceGroup(self, ctx:SQLParser.DropResourceGroupContext):
        pass


    # Enter a parse tree produced by SQLParser#utilityStatement.
    def enterUtilityStatement(self, ctx:SQLParser.UtilityStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#utilityStatement.
    def exitUtilityStatement(self, ctx:SQLParser.UtilityStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#describeStatement.
    def enterDescribeStatement(self, ctx:SQLParser.DescribeStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#describeStatement.
    def exitDescribeStatement(self, ctx:SQLParser.DescribeStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#explainStatement.
    def enterExplainStatement(self, ctx:SQLParser.ExplainStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#explainStatement.
    def exitExplainStatement(self, ctx:SQLParser.ExplainStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#explainableStatement.
    def enterExplainableStatement(self, ctx:SQLParser.ExplainableStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#explainableStatement.
    def exitExplainableStatement(self, ctx:SQLParser.ExplainableStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#helpCommand.
    def enterHelpCommand(self, ctx:SQLParser.HelpCommandContext):
        pass

    # Exit a parse tree produced by SQLParser#helpCommand.
    def exitHelpCommand(self, ctx:SQLParser.HelpCommandContext):
        pass


    # Enter a parse tree produced by SQLParser#useCommand.
    def enterUseCommand(self, ctx:SQLParser.UseCommandContext):
        pass

    # Exit a parse tree produced by SQLParser#useCommand.
    def exitUseCommand(self, ctx:SQLParser.UseCommandContext):
        pass


    # Enter a parse tree produced by SQLParser#restartServer.
    def enterRestartServer(self, ctx:SQLParser.RestartServerContext):
        pass

    # Exit a parse tree produced by SQLParser#restartServer.
    def exitRestartServer(self, ctx:SQLParser.RestartServerContext):
        pass


    # Enter a parse tree produced by SQLParser#exprOr.
    def enterExprOr(self, ctx:SQLParser.ExprOrContext):
        pass

    # Exit a parse tree produced by SQLParser#exprOr.
    def exitExprOr(self, ctx:SQLParser.ExprOrContext):
        pass


    # Enter a parse tree produced by SQLParser#exprNot.
    def enterExprNot(self, ctx:SQLParser.ExprNotContext):
        pass

    # Exit a parse tree produced by SQLParser#exprNot.
    def exitExprNot(self, ctx:SQLParser.ExprNotContext):
        pass


    # Enter a parse tree produced by SQLParser#exprIs.
    def enterExprIs(self, ctx:SQLParser.ExprIsContext):
        pass

    # Exit a parse tree produced by SQLParser#exprIs.
    def exitExprIs(self, ctx:SQLParser.ExprIsContext):
        pass


    # Enter a parse tree produced by SQLParser#exprAnd.
    def enterExprAnd(self, ctx:SQLParser.ExprAndContext):
        pass

    # Exit a parse tree produced by SQLParser#exprAnd.
    def exitExprAnd(self, ctx:SQLParser.ExprAndContext):
        pass


    # Enter a parse tree produced by SQLParser#exprXor.
    def enterExprXor(self, ctx:SQLParser.ExprXorContext):
        pass

    # Exit a parse tree produced by SQLParser#exprXor.
    def exitExprXor(self, ctx:SQLParser.ExprXorContext):
        pass


    # Enter a parse tree produced by SQLParser#primaryExprPredicate.
    def enterPrimaryExprPredicate(self, ctx:SQLParser.PrimaryExprPredicateContext):
        pass

    # Exit a parse tree produced by SQLParser#primaryExprPredicate.
    def exitPrimaryExprPredicate(self, ctx:SQLParser.PrimaryExprPredicateContext):
        pass


    # Enter a parse tree produced by SQLParser#primaryExprCompare.
    def enterPrimaryExprCompare(self, ctx:SQLParser.PrimaryExprCompareContext):
        pass

    # Exit a parse tree produced by SQLParser#primaryExprCompare.
    def exitPrimaryExprCompare(self, ctx:SQLParser.PrimaryExprCompareContext):
        pass


    # Enter a parse tree produced by SQLParser#primaryExprAllAny.
    def enterPrimaryExprAllAny(self, ctx:SQLParser.PrimaryExprAllAnyContext):
        pass

    # Exit a parse tree produced by SQLParser#primaryExprAllAny.
    def exitPrimaryExprAllAny(self, ctx:SQLParser.PrimaryExprAllAnyContext):
        pass


    # Enter a parse tree produced by SQLParser#primaryExprIsNull.
    def enterPrimaryExprIsNull(self, ctx:SQLParser.PrimaryExprIsNullContext):
        pass

    # Exit a parse tree produced by SQLParser#primaryExprIsNull.
    def exitPrimaryExprIsNull(self, ctx:SQLParser.PrimaryExprIsNullContext):
        pass


    # Enter a parse tree produced by SQLParser#compOp.
    def enterCompOp(self, ctx:SQLParser.CompOpContext):
        pass

    # Exit a parse tree produced by SQLParser#compOp.
    def exitCompOp(self, ctx:SQLParser.CompOpContext):
        pass


    # Enter a parse tree produced by SQLParser#predicate.
    def enterPredicate(self, ctx:SQLParser.PredicateContext):
        pass

    # Exit a parse tree produced by SQLParser#predicate.
    def exitPredicate(self, ctx:SQLParser.PredicateContext):
        pass


    # Enter a parse tree produced by SQLParser#predicateExprIn.
    def enterPredicateExprIn(self, ctx:SQLParser.PredicateExprInContext):
        pass

    # Exit a parse tree produced by SQLParser#predicateExprIn.
    def exitPredicateExprIn(self, ctx:SQLParser.PredicateExprInContext):
        pass


    # Enter a parse tree produced by SQLParser#predicateExprBetween.
    def enterPredicateExprBetween(self, ctx:SQLParser.PredicateExprBetweenContext):
        pass

    # Exit a parse tree produced by SQLParser#predicateExprBetween.
    def exitPredicateExprBetween(self, ctx:SQLParser.PredicateExprBetweenContext):
        pass


    # Enter a parse tree produced by SQLParser#predicateExprLike.
    def enterPredicateExprLike(self, ctx:SQLParser.PredicateExprLikeContext):
        pass

    # Exit a parse tree produced by SQLParser#predicateExprLike.
    def exitPredicateExprLike(self, ctx:SQLParser.PredicateExprLikeContext):
        pass


    # Enter a parse tree produced by SQLParser#predicateExprRegex.
    def enterPredicateExprRegex(self, ctx:SQLParser.PredicateExprRegexContext):
        pass

    # Exit a parse tree produced by SQLParser#predicateExprRegex.
    def exitPredicateExprRegex(self, ctx:SQLParser.PredicateExprRegexContext):
        pass


    # Enter a parse tree produced by SQLParser#bitExpr.
    def enterBitExpr(self, ctx:SQLParser.BitExprContext):
        pass

    # Exit a parse tree produced by SQLParser#bitExpr.
    def exitBitExpr(self, ctx:SQLParser.BitExprContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprConvert.
    def enterSimpleExprConvert(self, ctx:SQLParser.SimpleExprConvertContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprConvert.
    def exitSimpleExprConvert(self, ctx:SQLParser.SimpleExprConvertContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprVariable.
    def enterSimpleExprVariable(self, ctx:SQLParser.SimpleExprVariableContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprVariable.
    def exitSimpleExprVariable(self, ctx:SQLParser.SimpleExprVariableContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprCast.
    def enterSimpleExprCast(self, ctx:SQLParser.SimpleExprCastContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprCast.
    def exitSimpleExprCast(self, ctx:SQLParser.SimpleExprCastContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprUnary.
    def enterSimpleExprUnary(self, ctx:SQLParser.SimpleExprUnaryContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprUnary.
    def exitSimpleExprUnary(self, ctx:SQLParser.SimpleExprUnaryContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprOdbc.
    def enterSimpleExprOdbc(self, ctx:SQLParser.SimpleExprOdbcContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprOdbc.
    def exitSimpleExprOdbc(self, ctx:SQLParser.SimpleExprOdbcContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprRuntimeFunction.
    def enterSimpleExprRuntimeFunction(self, ctx:SQLParser.SimpleExprRuntimeFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprRuntimeFunction.
    def exitSimpleExprRuntimeFunction(self, ctx:SQLParser.SimpleExprRuntimeFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprFunction.
    def enterSimpleExprFunction(self, ctx:SQLParser.SimpleExprFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprFunction.
    def exitSimpleExprFunction(self, ctx:SQLParser.SimpleExprFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprCollate.
    def enterSimpleExprCollate(self, ctx:SQLParser.SimpleExprCollateContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprCollate.
    def exitSimpleExprCollate(self, ctx:SQLParser.SimpleExprCollateContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprMatch.
    def enterSimpleExprMatch(self, ctx:SQLParser.SimpleExprMatchContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprMatch.
    def exitSimpleExprMatch(self, ctx:SQLParser.SimpleExprMatchContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprWindowingFunction.
    def enterSimpleExprWindowingFunction(self, ctx:SQLParser.SimpleExprWindowingFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprWindowingFunction.
    def exitSimpleExprWindowingFunction(self, ctx:SQLParser.SimpleExprWindowingFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprBinary.
    def enterSimpleExprBinary(self, ctx:SQLParser.SimpleExprBinaryContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprBinary.
    def exitSimpleExprBinary(self, ctx:SQLParser.SimpleExprBinaryContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprColumnRef.
    def enterSimpleExprColumnRef(self, ctx:SQLParser.SimpleExprColumnRefContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprColumnRef.
    def exitSimpleExprColumnRef(self, ctx:SQLParser.SimpleExprColumnRefContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprParamMarker.
    def enterSimpleExprParamMarker(self, ctx:SQLParser.SimpleExprParamMarkerContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprParamMarker.
    def exitSimpleExprParamMarker(self, ctx:SQLParser.SimpleExprParamMarkerContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprSum.
    def enterSimpleExprSum(self, ctx:SQLParser.SimpleExprSumContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprSum.
    def exitSimpleExprSum(self, ctx:SQLParser.SimpleExprSumContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprConvertUsing.
    def enterSimpleExprConvertUsing(self, ctx:SQLParser.SimpleExprConvertUsingContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprConvertUsing.
    def exitSimpleExprConvertUsing(self, ctx:SQLParser.SimpleExprConvertUsingContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprSubQuery.
    def enterSimpleExprSubQuery(self, ctx:SQLParser.SimpleExprSubQueryContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprSubQuery.
    def exitSimpleExprSubQuery(self, ctx:SQLParser.SimpleExprSubQueryContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprGroupingOperation.
    def enterSimpleExprGroupingOperation(self, ctx:SQLParser.SimpleExprGroupingOperationContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprGroupingOperation.
    def exitSimpleExprGroupingOperation(self, ctx:SQLParser.SimpleExprGroupingOperationContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprNot.
    def enterSimpleExprNot(self, ctx:SQLParser.SimpleExprNotContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprNot.
    def exitSimpleExprNot(self, ctx:SQLParser.SimpleExprNotContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprValues.
    def enterSimpleExprValues(self, ctx:SQLParser.SimpleExprValuesContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprValues.
    def exitSimpleExprValues(self, ctx:SQLParser.SimpleExprValuesContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprDefault.
    def enterSimpleExprDefault(self, ctx:SQLParser.SimpleExprDefaultContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprDefault.
    def exitSimpleExprDefault(self, ctx:SQLParser.SimpleExprDefaultContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprList.
    def enterSimpleExprList(self, ctx:SQLParser.SimpleExprListContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprList.
    def exitSimpleExprList(self, ctx:SQLParser.SimpleExprListContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprInterval.
    def enterSimpleExprInterval(self, ctx:SQLParser.SimpleExprIntervalContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprInterval.
    def exitSimpleExprInterval(self, ctx:SQLParser.SimpleExprIntervalContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprCase.
    def enterSimpleExprCase(self, ctx:SQLParser.SimpleExprCaseContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprCase.
    def exitSimpleExprCase(self, ctx:SQLParser.SimpleExprCaseContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprConcat.
    def enterSimpleExprConcat(self, ctx:SQLParser.SimpleExprConcatContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprConcat.
    def exitSimpleExprConcat(self, ctx:SQLParser.SimpleExprConcatContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprLiteral.
    def enterSimpleExprLiteral(self, ctx:SQLParser.SimpleExprLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprLiteral.
    def exitSimpleExprLiteral(self, ctx:SQLParser.SimpleExprLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#arrayCast.
    def enterArrayCast(self, ctx:SQLParser.ArrayCastContext):
        pass

    # Exit a parse tree produced by SQLParser#arrayCast.
    def exitArrayCast(self, ctx:SQLParser.ArrayCastContext):
        pass


    # Enter a parse tree produced by SQLParser#jsonOperator.
    def enterJsonOperator(self, ctx:SQLParser.JsonOperatorContext):
        pass

    # Exit a parse tree produced by SQLParser#jsonOperator.
    def exitJsonOperator(self, ctx:SQLParser.JsonOperatorContext):
        pass


    # Enter a parse tree produced by SQLParser#sumExpr.
    def enterSumExpr(self, ctx:SQLParser.SumExprContext):
        pass

    # Exit a parse tree produced by SQLParser#sumExpr.
    def exitSumExpr(self, ctx:SQLParser.SumExprContext):
        pass


    # Enter a parse tree produced by SQLParser#groupingOperation.
    def enterGroupingOperation(self, ctx:SQLParser.GroupingOperationContext):
        pass

    # Exit a parse tree produced by SQLParser#groupingOperation.
    def exitGroupingOperation(self, ctx:SQLParser.GroupingOperationContext):
        pass


    # Enter a parse tree produced by SQLParser#windowFunctionCall.
    def enterWindowFunctionCall(self, ctx:SQLParser.WindowFunctionCallContext):
        pass

    # Exit a parse tree produced by SQLParser#windowFunctionCall.
    def exitWindowFunctionCall(self, ctx:SQLParser.WindowFunctionCallContext):
        pass


    # Enter a parse tree produced by SQLParser#windowingClause.
    def enterWindowingClause(self, ctx:SQLParser.WindowingClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#windowingClause.
    def exitWindowingClause(self, ctx:SQLParser.WindowingClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#leadLagInfo.
    def enterLeadLagInfo(self, ctx:SQLParser.LeadLagInfoContext):
        pass

    # Exit a parse tree produced by SQLParser#leadLagInfo.
    def exitLeadLagInfo(self, ctx:SQLParser.LeadLagInfoContext):
        pass


    # Enter a parse tree produced by SQLParser#nullTreatment.
    def enterNullTreatment(self, ctx:SQLParser.NullTreatmentContext):
        pass

    # Exit a parse tree produced by SQLParser#nullTreatment.
    def exitNullTreatment(self, ctx:SQLParser.NullTreatmentContext):
        pass


    # Enter a parse tree produced by SQLParser#jsonFunction.
    def enterJsonFunction(self, ctx:SQLParser.JsonFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#jsonFunction.
    def exitJsonFunction(self, ctx:SQLParser.JsonFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#inSumExpr.
    def enterInSumExpr(self, ctx:SQLParser.InSumExprContext):
        pass

    # Exit a parse tree produced by SQLParser#inSumExpr.
    def exitInSumExpr(self, ctx:SQLParser.InSumExprContext):
        pass


    # Enter a parse tree produced by SQLParser#identListArg.
    def enterIdentListArg(self, ctx:SQLParser.IdentListArgContext):
        pass

    # Exit a parse tree produced by SQLParser#identListArg.
    def exitIdentListArg(self, ctx:SQLParser.IdentListArgContext):
        pass


    # Enter a parse tree produced by SQLParser#identList.
    def enterIdentList(self, ctx:SQLParser.IdentListContext):
        pass

    # Exit a parse tree produced by SQLParser#identList.
    def exitIdentList(self, ctx:SQLParser.IdentListContext):
        pass


    # Enter a parse tree produced by SQLParser#fulltextOptions.
    def enterFulltextOptions(self, ctx:SQLParser.FulltextOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#fulltextOptions.
    def exitFulltextOptions(self, ctx:SQLParser.FulltextOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#runtimeFunctionCall.
    def enterRuntimeFunctionCall(self, ctx:SQLParser.RuntimeFunctionCallContext):
        pass

    # Exit a parse tree produced by SQLParser#runtimeFunctionCall.
    def exitRuntimeFunctionCall(self, ctx:SQLParser.RuntimeFunctionCallContext):
        pass


    # Enter a parse tree produced by SQLParser#geometryFunction.
    def enterGeometryFunction(self, ctx:SQLParser.GeometryFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#geometryFunction.
    def exitGeometryFunction(self, ctx:SQLParser.GeometryFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#timeFunctionParameters.
    def enterTimeFunctionParameters(self, ctx:SQLParser.TimeFunctionParametersContext):
        pass

    # Exit a parse tree produced by SQLParser#timeFunctionParameters.
    def exitTimeFunctionParameters(self, ctx:SQLParser.TimeFunctionParametersContext):
        pass


    # Enter a parse tree produced by SQLParser#fractionalPrecision.
    def enterFractionalPrecision(self, ctx:SQLParser.FractionalPrecisionContext):
        pass

    # Exit a parse tree produced by SQLParser#fractionalPrecision.
    def exitFractionalPrecision(self, ctx:SQLParser.FractionalPrecisionContext):
        pass


    # Enter a parse tree produced by SQLParser#weightStringLevels.
    def enterWeightStringLevels(self, ctx:SQLParser.WeightStringLevelsContext):
        pass

    # Exit a parse tree produced by SQLParser#weightStringLevels.
    def exitWeightStringLevels(self, ctx:SQLParser.WeightStringLevelsContext):
        pass


    # Enter a parse tree produced by SQLParser#weightStringLevelListItem.
    def enterWeightStringLevelListItem(self, ctx:SQLParser.WeightStringLevelListItemContext):
        pass

    # Exit a parse tree produced by SQLParser#weightStringLevelListItem.
    def exitWeightStringLevelListItem(self, ctx:SQLParser.WeightStringLevelListItemContext):
        pass


    # Enter a parse tree produced by SQLParser#dateTimeTtype.
    def enterDateTimeTtype(self, ctx:SQLParser.DateTimeTtypeContext):
        pass

    # Exit a parse tree produced by SQLParser#dateTimeTtype.
    def exitDateTimeTtype(self, ctx:SQLParser.DateTimeTtypeContext):
        pass


    # Enter a parse tree produced by SQLParser#trimFunction.
    def enterTrimFunction(self, ctx:SQLParser.TrimFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#trimFunction.
    def exitTrimFunction(self, ctx:SQLParser.TrimFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#substringFunction.
    def enterSubstringFunction(self, ctx:SQLParser.SubstringFunctionContext):
        pass

    # Exit a parse tree produced by SQLParser#substringFunction.
    def exitSubstringFunction(self, ctx:SQLParser.SubstringFunctionContext):
        pass


    # Enter a parse tree produced by SQLParser#functionCall.
    def enterFunctionCall(self, ctx:SQLParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by SQLParser#functionCall.
    def exitFunctionCall(self, ctx:SQLParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by SQLParser#udfExprList.
    def enterUdfExprList(self, ctx:SQLParser.UdfExprListContext):
        pass

    # Exit a parse tree produced by SQLParser#udfExprList.
    def exitUdfExprList(self, ctx:SQLParser.UdfExprListContext):
        pass


    # Enter a parse tree produced by SQLParser#udfExpr.
    def enterUdfExpr(self, ctx:SQLParser.UdfExprContext):
        pass

    # Exit a parse tree produced by SQLParser#udfExpr.
    def exitUdfExpr(self, ctx:SQLParser.UdfExprContext):
        pass


    # Enter a parse tree produced by SQLParser#variable.
    def enterVariable(self, ctx:SQLParser.VariableContext):
        pass

    # Exit a parse tree produced by SQLParser#variable.
    def exitVariable(self, ctx:SQLParser.VariableContext):
        pass


    # Enter a parse tree produced by SQLParser#userVariable.
    def enterUserVariable(self, ctx:SQLParser.UserVariableContext):
        pass

    # Exit a parse tree produced by SQLParser#userVariable.
    def exitUserVariable(self, ctx:SQLParser.UserVariableContext):
        pass


    # Enter a parse tree produced by SQLParser#systemVariable.
    def enterSystemVariable(self, ctx:SQLParser.SystemVariableContext):
        pass

    # Exit a parse tree produced by SQLParser#systemVariable.
    def exitSystemVariable(self, ctx:SQLParser.SystemVariableContext):
        pass


    # Enter a parse tree produced by SQLParser#internalVariableName.
    def enterInternalVariableName(self, ctx:SQLParser.InternalVariableNameContext):
        pass

    # Exit a parse tree produced by SQLParser#internalVariableName.
    def exitInternalVariableName(self, ctx:SQLParser.InternalVariableNameContext):
        pass


    # Enter a parse tree produced by SQLParser#whenExpression.
    def enterWhenExpression(self, ctx:SQLParser.WhenExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#whenExpression.
    def exitWhenExpression(self, ctx:SQLParser.WhenExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#thenExpression.
    def enterThenExpression(self, ctx:SQLParser.ThenExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#thenExpression.
    def exitThenExpression(self, ctx:SQLParser.ThenExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#elseExpression.
    def enterElseExpression(self, ctx:SQLParser.ElseExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#elseExpression.
    def exitElseExpression(self, ctx:SQLParser.ElseExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#castType.
    def enterCastType(self, ctx:SQLParser.CastTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#castType.
    def exitCastType(self, ctx:SQLParser.CastTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#exprList.
    def enterExprList(self, ctx:SQLParser.ExprListContext):
        pass

    # Exit a parse tree produced by SQLParser#exprList.
    def exitExprList(self, ctx:SQLParser.ExprListContext):
        pass


    # Enter a parse tree produced by SQLParser#charset.
    def enterCharset(self, ctx:SQLParser.CharsetContext):
        pass

    # Exit a parse tree produced by SQLParser#charset.
    def exitCharset(self, ctx:SQLParser.CharsetContext):
        pass


    # Enter a parse tree produced by SQLParser#notRule.
    def enterNotRule(self, ctx:SQLParser.NotRuleContext):
        pass

    # Exit a parse tree produced by SQLParser#notRule.
    def exitNotRule(self, ctx:SQLParser.NotRuleContext):
        pass


    # Enter a parse tree produced by SQLParser#not2Rule.
    def enterNot2Rule(self, ctx:SQLParser.Not2RuleContext):
        pass

    # Exit a parse tree produced by SQLParser#not2Rule.
    def exitNot2Rule(self, ctx:SQLParser.Not2RuleContext):
        pass


    # Enter a parse tree produced by SQLParser#interval.
    def enterInterval(self, ctx:SQLParser.IntervalContext):
        pass

    # Exit a parse tree produced by SQLParser#interval.
    def exitInterval(self, ctx:SQLParser.IntervalContext):
        pass


    # Enter a parse tree produced by SQLParser#intervalTimeStamp.
    def enterIntervalTimeStamp(self, ctx:SQLParser.IntervalTimeStampContext):
        pass

    # Exit a parse tree produced by SQLParser#intervalTimeStamp.
    def exitIntervalTimeStamp(self, ctx:SQLParser.IntervalTimeStampContext):
        pass


    # Enter a parse tree produced by SQLParser#exprListWithParentheses.
    def enterExprListWithParentheses(self, ctx:SQLParser.ExprListWithParenthesesContext):
        pass

    # Exit a parse tree produced by SQLParser#exprListWithParentheses.
    def exitExprListWithParentheses(self, ctx:SQLParser.ExprListWithParenthesesContext):
        pass


    # Enter a parse tree produced by SQLParser#exprWithParentheses.
    def enterExprWithParentheses(self, ctx:SQLParser.ExprWithParenthesesContext):
        pass

    # Exit a parse tree produced by SQLParser#exprWithParentheses.
    def exitExprWithParentheses(self, ctx:SQLParser.ExprWithParenthesesContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleExprWithParentheses.
    def enterSimpleExprWithParentheses(self, ctx:SQLParser.SimpleExprWithParenthesesContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleExprWithParentheses.
    def exitSimpleExprWithParentheses(self, ctx:SQLParser.SimpleExprWithParenthesesContext):
        pass


    # Enter a parse tree produced by SQLParser#orderList.
    def enterOrderList(self, ctx:SQLParser.OrderListContext):
        pass

    # Exit a parse tree produced by SQLParser#orderList.
    def exitOrderList(self, ctx:SQLParser.OrderListContext):
        pass


    # Enter a parse tree produced by SQLParser#orderExpression.
    def enterOrderExpression(self, ctx:SQLParser.OrderExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#orderExpression.
    def exitOrderExpression(self, ctx:SQLParser.OrderExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#groupList.
    def enterGroupList(self, ctx:SQLParser.GroupListContext):
        pass

    # Exit a parse tree produced by SQLParser#groupList.
    def exitGroupList(self, ctx:SQLParser.GroupListContext):
        pass


    # Enter a parse tree produced by SQLParser#groupingExpression.
    def enterGroupingExpression(self, ctx:SQLParser.GroupingExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#groupingExpression.
    def exitGroupingExpression(self, ctx:SQLParser.GroupingExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#channel.
    def enterChannel(self, ctx:SQLParser.ChannelContext):
        pass

    # Exit a parse tree produced by SQLParser#channel.
    def exitChannel(self, ctx:SQLParser.ChannelContext):
        pass


    # Enter a parse tree produced by SQLParser#compoundStatement.
    def enterCompoundStatement(self, ctx:SQLParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#compoundStatement.
    def exitCompoundStatement(self, ctx:SQLParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#returnStatement.
    def enterReturnStatement(self, ctx:SQLParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#returnStatement.
    def exitReturnStatement(self, ctx:SQLParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#ifStatement.
    def enterIfStatement(self, ctx:SQLParser.IfStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#ifStatement.
    def exitIfStatement(self, ctx:SQLParser.IfStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#ifBody.
    def enterIfBody(self, ctx:SQLParser.IfBodyContext):
        pass

    # Exit a parse tree produced by SQLParser#ifBody.
    def exitIfBody(self, ctx:SQLParser.IfBodyContext):
        pass


    # Enter a parse tree produced by SQLParser#thenStatement.
    def enterThenStatement(self, ctx:SQLParser.ThenStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#thenStatement.
    def exitThenStatement(self, ctx:SQLParser.ThenStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#compoundStatementList.
    def enterCompoundStatementList(self, ctx:SQLParser.CompoundStatementListContext):
        pass

    # Exit a parse tree produced by SQLParser#compoundStatementList.
    def exitCompoundStatementList(self, ctx:SQLParser.CompoundStatementListContext):
        pass


    # Enter a parse tree produced by SQLParser#caseStatement.
    def enterCaseStatement(self, ctx:SQLParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#caseStatement.
    def exitCaseStatement(self, ctx:SQLParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#elseStatement.
    def enterElseStatement(self, ctx:SQLParser.ElseStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#elseStatement.
    def exitElseStatement(self, ctx:SQLParser.ElseStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#labeledBlock.
    def enterLabeledBlock(self, ctx:SQLParser.LabeledBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#labeledBlock.
    def exitLabeledBlock(self, ctx:SQLParser.LabeledBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#unlabeledBlock.
    def enterUnlabeledBlock(self, ctx:SQLParser.UnlabeledBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#unlabeledBlock.
    def exitUnlabeledBlock(self, ctx:SQLParser.UnlabeledBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#label.
    def enterLabel(self, ctx:SQLParser.LabelContext):
        pass

    # Exit a parse tree produced by SQLParser#label.
    def exitLabel(self, ctx:SQLParser.LabelContext):
        pass


    # Enter a parse tree produced by SQLParser#beginEndBlock.
    def enterBeginEndBlock(self, ctx:SQLParser.BeginEndBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#beginEndBlock.
    def exitBeginEndBlock(self, ctx:SQLParser.BeginEndBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#labeledControl.
    def enterLabeledControl(self, ctx:SQLParser.LabeledControlContext):
        pass

    # Exit a parse tree produced by SQLParser#labeledControl.
    def exitLabeledControl(self, ctx:SQLParser.LabeledControlContext):
        pass


    # Enter a parse tree produced by SQLParser#unlabeledControl.
    def enterUnlabeledControl(self, ctx:SQLParser.UnlabeledControlContext):
        pass

    # Exit a parse tree produced by SQLParser#unlabeledControl.
    def exitUnlabeledControl(self, ctx:SQLParser.UnlabeledControlContext):
        pass


    # Enter a parse tree produced by SQLParser#loopBlock.
    def enterLoopBlock(self, ctx:SQLParser.LoopBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#loopBlock.
    def exitLoopBlock(self, ctx:SQLParser.LoopBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#whileDoBlock.
    def enterWhileDoBlock(self, ctx:SQLParser.WhileDoBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#whileDoBlock.
    def exitWhileDoBlock(self, ctx:SQLParser.WhileDoBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#repeatUntilBlock.
    def enterRepeatUntilBlock(self, ctx:SQLParser.RepeatUntilBlockContext):
        pass

    # Exit a parse tree produced by SQLParser#repeatUntilBlock.
    def exitRepeatUntilBlock(self, ctx:SQLParser.RepeatUntilBlockContext):
        pass


    # Enter a parse tree produced by SQLParser#spDeclarations.
    def enterSpDeclarations(self, ctx:SQLParser.SpDeclarationsContext):
        pass

    # Exit a parse tree produced by SQLParser#spDeclarations.
    def exitSpDeclarations(self, ctx:SQLParser.SpDeclarationsContext):
        pass


    # Enter a parse tree produced by SQLParser#spDeclaration.
    def enterSpDeclaration(self, ctx:SQLParser.SpDeclarationContext):
        pass

    # Exit a parse tree produced by SQLParser#spDeclaration.
    def exitSpDeclaration(self, ctx:SQLParser.SpDeclarationContext):
        pass


    # Enter a parse tree produced by SQLParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:SQLParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by SQLParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:SQLParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by SQLParser#conditionDeclaration.
    def enterConditionDeclaration(self, ctx:SQLParser.ConditionDeclarationContext):
        pass

    # Exit a parse tree produced by SQLParser#conditionDeclaration.
    def exitConditionDeclaration(self, ctx:SQLParser.ConditionDeclarationContext):
        pass


    # Enter a parse tree produced by SQLParser#spCondition.
    def enterSpCondition(self, ctx:SQLParser.SpConditionContext):
        pass

    # Exit a parse tree produced by SQLParser#spCondition.
    def exitSpCondition(self, ctx:SQLParser.SpConditionContext):
        pass


    # Enter a parse tree produced by SQLParser#sqlstate.
    def enterSqlstate(self, ctx:SQLParser.SqlstateContext):
        pass

    # Exit a parse tree produced by SQLParser#sqlstate.
    def exitSqlstate(self, ctx:SQLParser.SqlstateContext):
        pass


    # Enter a parse tree produced by SQLParser#handlerDeclaration.
    def enterHandlerDeclaration(self, ctx:SQLParser.HandlerDeclarationContext):
        pass

    # Exit a parse tree produced by SQLParser#handlerDeclaration.
    def exitHandlerDeclaration(self, ctx:SQLParser.HandlerDeclarationContext):
        pass


    # Enter a parse tree produced by SQLParser#handlerCondition.
    def enterHandlerCondition(self, ctx:SQLParser.HandlerConditionContext):
        pass

    # Exit a parse tree produced by SQLParser#handlerCondition.
    def exitHandlerCondition(self, ctx:SQLParser.HandlerConditionContext):
        pass


    # Enter a parse tree produced by SQLParser#cursorDeclaration.
    def enterCursorDeclaration(self, ctx:SQLParser.CursorDeclarationContext):
        pass

    # Exit a parse tree produced by SQLParser#cursorDeclaration.
    def exitCursorDeclaration(self, ctx:SQLParser.CursorDeclarationContext):
        pass


    # Enter a parse tree produced by SQLParser#iterateStatement.
    def enterIterateStatement(self, ctx:SQLParser.IterateStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#iterateStatement.
    def exitIterateStatement(self, ctx:SQLParser.IterateStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#leaveStatement.
    def enterLeaveStatement(self, ctx:SQLParser.LeaveStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#leaveStatement.
    def exitLeaveStatement(self, ctx:SQLParser.LeaveStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#getDiagnostics.
    def enterGetDiagnostics(self, ctx:SQLParser.GetDiagnosticsContext):
        pass

    # Exit a parse tree produced by SQLParser#getDiagnostics.
    def exitGetDiagnostics(self, ctx:SQLParser.GetDiagnosticsContext):
        pass


    # Enter a parse tree produced by SQLParser#signalAllowedExpr.
    def enterSignalAllowedExpr(self, ctx:SQLParser.SignalAllowedExprContext):
        pass

    # Exit a parse tree produced by SQLParser#signalAllowedExpr.
    def exitSignalAllowedExpr(self, ctx:SQLParser.SignalAllowedExprContext):
        pass


    # Enter a parse tree produced by SQLParser#statementInformationItem.
    def enterStatementInformationItem(self, ctx:SQLParser.StatementInformationItemContext):
        pass

    # Exit a parse tree produced by SQLParser#statementInformationItem.
    def exitStatementInformationItem(self, ctx:SQLParser.StatementInformationItemContext):
        pass


    # Enter a parse tree produced by SQLParser#conditionInformationItem.
    def enterConditionInformationItem(self, ctx:SQLParser.ConditionInformationItemContext):
        pass

    # Exit a parse tree produced by SQLParser#conditionInformationItem.
    def exitConditionInformationItem(self, ctx:SQLParser.ConditionInformationItemContext):
        pass


    # Enter a parse tree produced by SQLParser#signalInformationItemName.
    def enterSignalInformationItemName(self, ctx:SQLParser.SignalInformationItemNameContext):
        pass

    # Exit a parse tree produced by SQLParser#signalInformationItemName.
    def exitSignalInformationItemName(self, ctx:SQLParser.SignalInformationItemNameContext):
        pass


    # Enter a parse tree produced by SQLParser#signalStatement.
    def enterSignalStatement(self, ctx:SQLParser.SignalStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#signalStatement.
    def exitSignalStatement(self, ctx:SQLParser.SignalStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#resignalStatement.
    def enterResignalStatement(self, ctx:SQLParser.ResignalStatementContext):
        pass

    # Exit a parse tree produced by SQLParser#resignalStatement.
    def exitResignalStatement(self, ctx:SQLParser.ResignalStatementContext):
        pass


    # Enter a parse tree produced by SQLParser#signalInformationItem.
    def enterSignalInformationItem(self, ctx:SQLParser.SignalInformationItemContext):
        pass

    # Exit a parse tree produced by SQLParser#signalInformationItem.
    def exitSignalInformationItem(self, ctx:SQLParser.SignalInformationItemContext):
        pass


    # Enter a parse tree produced by SQLParser#cursorOpen.
    def enterCursorOpen(self, ctx:SQLParser.CursorOpenContext):
        pass

    # Exit a parse tree produced by SQLParser#cursorOpen.
    def exitCursorOpen(self, ctx:SQLParser.CursorOpenContext):
        pass


    # Enter a parse tree produced by SQLParser#cursorClose.
    def enterCursorClose(self, ctx:SQLParser.CursorCloseContext):
        pass

    # Exit a parse tree produced by SQLParser#cursorClose.
    def exitCursorClose(self, ctx:SQLParser.CursorCloseContext):
        pass


    # Enter a parse tree produced by SQLParser#cursorFetch.
    def enterCursorFetch(self, ctx:SQLParser.CursorFetchContext):
        pass

    # Exit a parse tree produced by SQLParser#cursorFetch.
    def exitCursorFetch(self, ctx:SQLParser.CursorFetchContext):
        pass


    # Enter a parse tree produced by SQLParser#schedule.
    def enterSchedule(self, ctx:SQLParser.ScheduleContext):
        pass

    # Exit a parse tree produced by SQLParser#schedule.
    def exitSchedule(self, ctx:SQLParser.ScheduleContext):
        pass


    # Enter a parse tree produced by SQLParser#columnDefinition.
    def enterColumnDefinition(self, ctx:SQLParser.ColumnDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#columnDefinition.
    def exitColumnDefinition(self, ctx:SQLParser.ColumnDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#checkOrReferences.
    def enterCheckOrReferences(self, ctx:SQLParser.CheckOrReferencesContext):
        pass

    # Exit a parse tree produced by SQLParser#checkOrReferences.
    def exitCheckOrReferences(self, ctx:SQLParser.CheckOrReferencesContext):
        pass


    # Enter a parse tree produced by SQLParser#checkConstraint.
    def enterCheckConstraint(self, ctx:SQLParser.CheckConstraintContext):
        pass

    # Exit a parse tree produced by SQLParser#checkConstraint.
    def exitCheckConstraint(self, ctx:SQLParser.CheckConstraintContext):
        pass


    # Enter a parse tree produced by SQLParser#constraintEnforcement.
    def enterConstraintEnforcement(self, ctx:SQLParser.ConstraintEnforcementContext):
        pass

    # Exit a parse tree produced by SQLParser#constraintEnforcement.
    def exitConstraintEnforcement(self, ctx:SQLParser.ConstraintEnforcementContext):
        pass


    # Enter a parse tree produced by SQLParser#tableConstraintDef.
    def enterTableConstraintDef(self, ctx:SQLParser.TableConstraintDefContext):
        pass

    # Exit a parse tree produced by SQLParser#tableConstraintDef.
    def exitTableConstraintDef(self, ctx:SQLParser.TableConstraintDefContext):
        pass


    # Enter a parse tree produced by SQLParser#constraintName.
    def enterConstraintName(self, ctx:SQLParser.ConstraintNameContext):
        pass

    # Exit a parse tree produced by SQLParser#constraintName.
    def exitConstraintName(self, ctx:SQLParser.ConstraintNameContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldDefinition.
    def enterFieldDefinition(self, ctx:SQLParser.FieldDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldDefinition.
    def exitFieldDefinition(self, ctx:SQLParser.FieldDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#columnAttribute.
    def enterColumnAttribute(self, ctx:SQLParser.ColumnAttributeContext):
        pass

    # Exit a parse tree produced by SQLParser#columnAttribute.
    def exitColumnAttribute(self, ctx:SQLParser.ColumnAttributeContext):
        pass


    # Enter a parse tree produced by SQLParser#columnFormat.
    def enterColumnFormat(self, ctx:SQLParser.ColumnFormatContext):
        pass

    # Exit a parse tree produced by SQLParser#columnFormat.
    def exitColumnFormat(self, ctx:SQLParser.ColumnFormatContext):
        pass


    # Enter a parse tree produced by SQLParser#storageMedia.
    def enterStorageMedia(self, ctx:SQLParser.StorageMediaContext):
        pass

    # Exit a parse tree produced by SQLParser#storageMedia.
    def exitStorageMedia(self, ctx:SQLParser.StorageMediaContext):
        pass


    # Enter a parse tree produced by SQLParser#gcolAttribute.
    def enterGcolAttribute(self, ctx:SQLParser.GcolAttributeContext):
        pass

    # Exit a parse tree produced by SQLParser#gcolAttribute.
    def exitGcolAttribute(self, ctx:SQLParser.GcolAttributeContext):
        pass


    # Enter a parse tree produced by SQLParser#references.
    def enterReferences(self, ctx:SQLParser.ReferencesContext):
        pass

    # Exit a parse tree produced by SQLParser#references.
    def exitReferences(self, ctx:SQLParser.ReferencesContext):
        pass


    # Enter a parse tree produced by SQLParser#deleteOption.
    def enterDeleteOption(self, ctx:SQLParser.DeleteOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#deleteOption.
    def exitDeleteOption(self, ctx:SQLParser.DeleteOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#keyList.
    def enterKeyList(self, ctx:SQLParser.KeyListContext):
        pass

    # Exit a parse tree produced by SQLParser#keyList.
    def exitKeyList(self, ctx:SQLParser.KeyListContext):
        pass


    # Enter a parse tree produced by SQLParser#keyPart.
    def enterKeyPart(self, ctx:SQLParser.KeyPartContext):
        pass

    # Exit a parse tree produced by SQLParser#keyPart.
    def exitKeyPart(self, ctx:SQLParser.KeyPartContext):
        pass


    # Enter a parse tree produced by SQLParser#keyListWithExpression.
    def enterKeyListWithExpression(self, ctx:SQLParser.KeyListWithExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#keyListWithExpression.
    def exitKeyListWithExpression(self, ctx:SQLParser.KeyListWithExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#keyPartOrExpression.
    def enterKeyPartOrExpression(self, ctx:SQLParser.KeyPartOrExpressionContext):
        pass

    # Exit a parse tree produced by SQLParser#keyPartOrExpression.
    def exitKeyPartOrExpression(self, ctx:SQLParser.KeyPartOrExpressionContext):
        pass


    # Enter a parse tree produced by SQLParser#keyListVariants.
    def enterKeyListVariants(self, ctx:SQLParser.KeyListVariantsContext):
        pass

    # Exit a parse tree produced by SQLParser#keyListVariants.
    def exitKeyListVariants(self, ctx:SQLParser.KeyListVariantsContext):
        pass


    # Enter a parse tree produced by SQLParser#indexType.
    def enterIndexType(self, ctx:SQLParser.IndexTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#indexType.
    def exitIndexType(self, ctx:SQLParser.IndexTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#indexOption.
    def enterIndexOption(self, ctx:SQLParser.IndexOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#indexOption.
    def exitIndexOption(self, ctx:SQLParser.IndexOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#commonIndexOption.
    def enterCommonIndexOption(self, ctx:SQLParser.CommonIndexOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#commonIndexOption.
    def exitCommonIndexOption(self, ctx:SQLParser.CommonIndexOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#visibility.
    def enterVisibility(self, ctx:SQLParser.VisibilityContext):
        pass

    # Exit a parse tree produced by SQLParser#visibility.
    def exitVisibility(self, ctx:SQLParser.VisibilityContext):
        pass


    # Enter a parse tree produced by SQLParser#indexTypeClause.
    def enterIndexTypeClause(self, ctx:SQLParser.IndexTypeClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#indexTypeClause.
    def exitIndexTypeClause(self, ctx:SQLParser.IndexTypeClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#fulltextIndexOption.
    def enterFulltextIndexOption(self, ctx:SQLParser.FulltextIndexOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#fulltextIndexOption.
    def exitFulltextIndexOption(self, ctx:SQLParser.FulltextIndexOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#spatialIndexOption.
    def enterSpatialIndexOption(self, ctx:SQLParser.SpatialIndexOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#spatialIndexOption.
    def exitSpatialIndexOption(self, ctx:SQLParser.SpatialIndexOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#dataTypeDefinition.
    def enterDataTypeDefinition(self, ctx:SQLParser.DataTypeDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#dataTypeDefinition.
    def exitDataTypeDefinition(self, ctx:SQLParser.DataTypeDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#dataType.
    def enterDataType(self, ctx:SQLParser.DataTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#dataType.
    def exitDataType(self, ctx:SQLParser.DataTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#nchar.
    def enterNchar(self, ctx:SQLParser.NcharContext):
        pass

    # Exit a parse tree produced by SQLParser#nchar.
    def exitNchar(self, ctx:SQLParser.NcharContext):
        pass


    # Enter a parse tree produced by SQLParser#realType.
    def enterRealType(self, ctx:SQLParser.RealTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#realType.
    def exitRealType(self, ctx:SQLParser.RealTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldLength.
    def enterFieldLength(self, ctx:SQLParser.FieldLengthContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldLength.
    def exitFieldLength(self, ctx:SQLParser.FieldLengthContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldOptions.
    def enterFieldOptions(self, ctx:SQLParser.FieldOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldOptions.
    def exitFieldOptions(self, ctx:SQLParser.FieldOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#charsetWithOptBinary.
    def enterCharsetWithOptBinary(self, ctx:SQLParser.CharsetWithOptBinaryContext):
        pass

    # Exit a parse tree produced by SQLParser#charsetWithOptBinary.
    def exitCharsetWithOptBinary(self, ctx:SQLParser.CharsetWithOptBinaryContext):
        pass


    # Enter a parse tree produced by SQLParser#ascii.
    def enterAscii(self, ctx:SQLParser.AsciiContext):
        pass

    # Exit a parse tree produced by SQLParser#ascii.
    def exitAscii(self, ctx:SQLParser.AsciiContext):
        pass


    # Enter a parse tree produced by SQLParser#unicode.
    def enterUnicode(self, ctx:SQLParser.UnicodeContext):
        pass

    # Exit a parse tree produced by SQLParser#unicode.
    def exitUnicode(self, ctx:SQLParser.UnicodeContext):
        pass


    # Enter a parse tree produced by SQLParser#wsNumCodepoints.
    def enterWsNumCodepoints(self, ctx:SQLParser.WsNumCodepointsContext):
        pass

    # Exit a parse tree produced by SQLParser#wsNumCodepoints.
    def exitWsNumCodepoints(self, ctx:SQLParser.WsNumCodepointsContext):
        pass


    # Enter a parse tree produced by SQLParser#typeDatetimePrecision.
    def enterTypeDatetimePrecision(self, ctx:SQLParser.TypeDatetimePrecisionContext):
        pass

    # Exit a parse tree produced by SQLParser#typeDatetimePrecision.
    def exitTypeDatetimePrecision(self, ctx:SQLParser.TypeDatetimePrecisionContext):
        pass


    # Enter a parse tree produced by SQLParser#charsetName.
    def enterCharsetName(self, ctx:SQLParser.CharsetNameContext):
        pass

    # Exit a parse tree produced by SQLParser#charsetName.
    def exitCharsetName(self, ctx:SQLParser.CharsetNameContext):
        pass


    # Enter a parse tree produced by SQLParser#collationName.
    def enterCollationName(self, ctx:SQLParser.CollationNameContext):
        pass

    # Exit a parse tree produced by SQLParser#collationName.
    def exitCollationName(self, ctx:SQLParser.CollationNameContext):
        pass


    # Enter a parse tree produced by SQLParser#createTableOptions.
    def enterCreateTableOptions(self, ctx:SQLParser.CreateTableOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#createTableOptions.
    def exitCreateTableOptions(self, ctx:SQLParser.CreateTableOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#createTableOptionsSpaceSeparated.
    def enterCreateTableOptionsSpaceSeparated(self, ctx:SQLParser.CreateTableOptionsSpaceSeparatedContext):
        pass

    # Exit a parse tree produced by SQLParser#createTableOptionsSpaceSeparated.
    def exitCreateTableOptionsSpaceSeparated(self, ctx:SQLParser.CreateTableOptionsSpaceSeparatedContext):
        pass


    # Enter a parse tree produced by SQLParser#createTableOption.
    def enterCreateTableOption(self, ctx:SQLParser.CreateTableOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#createTableOption.
    def exitCreateTableOption(self, ctx:SQLParser.CreateTableOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#ternaryOption.
    def enterTernaryOption(self, ctx:SQLParser.TernaryOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#ternaryOption.
    def exitTernaryOption(self, ctx:SQLParser.TernaryOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#defaultCollation.
    def enterDefaultCollation(self, ctx:SQLParser.DefaultCollationContext):
        pass

    # Exit a parse tree produced by SQLParser#defaultCollation.
    def exitDefaultCollation(self, ctx:SQLParser.DefaultCollationContext):
        pass


    # Enter a parse tree produced by SQLParser#defaultEncryption.
    def enterDefaultEncryption(self, ctx:SQLParser.DefaultEncryptionContext):
        pass

    # Exit a parse tree produced by SQLParser#defaultEncryption.
    def exitDefaultEncryption(self, ctx:SQLParser.DefaultEncryptionContext):
        pass


    # Enter a parse tree produced by SQLParser#defaultCharset.
    def enterDefaultCharset(self, ctx:SQLParser.DefaultCharsetContext):
        pass

    # Exit a parse tree produced by SQLParser#defaultCharset.
    def exitDefaultCharset(self, ctx:SQLParser.DefaultCharsetContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionClause.
    def enterPartitionClause(self, ctx:SQLParser.PartitionClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionClause.
    def exitPartitionClause(self, ctx:SQLParser.PartitionClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDefKey.
    def enterPartitionDefKey(self, ctx:SQLParser.PartitionDefKeyContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDefKey.
    def exitPartitionDefKey(self, ctx:SQLParser.PartitionDefKeyContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDefHash.
    def enterPartitionDefHash(self, ctx:SQLParser.PartitionDefHashContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDefHash.
    def exitPartitionDefHash(self, ctx:SQLParser.PartitionDefHashContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDefRangeList.
    def enterPartitionDefRangeList(self, ctx:SQLParser.PartitionDefRangeListContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDefRangeList.
    def exitPartitionDefRangeList(self, ctx:SQLParser.PartitionDefRangeListContext):
        pass


    # Enter a parse tree produced by SQLParser#subPartitions.
    def enterSubPartitions(self, ctx:SQLParser.SubPartitionsContext):
        pass

    # Exit a parse tree produced by SQLParser#subPartitions.
    def exitSubPartitions(self, ctx:SQLParser.SubPartitionsContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionKeyAlgorithm.
    def enterPartitionKeyAlgorithm(self, ctx:SQLParser.PartitionKeyAlgorithmContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionKeyAlgorithm.
    def exitPartitionKeyAlgorithm(self, ctx:SQLParser.PartitionKeyAlgorithmContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDefinitions.
    def enterPartitionDefinitions(self, ctx:SQLParser.PartitionDefinitionsContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDefinitions.
    def exitPartitionDefinitions(self, ctx:SQLParser.PartitionDefinitionsContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionDefinition.
    def enterPartitionDefinition(self, ctx:SQLParser.PartitionDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionDefinition.
    def exitPartitionDefinition(self, ctx:SQLParser.PartitionDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionValuesIn.
    def enterPartitionValuesIn(self, ctx:SQLParser.PartitionValuesInContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionValuesIn.
    def exitPartitionValuesIn(self, ctx:SQLParser.PartitionValuesInContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionOption.
    def enterPartitionOption(self, ctx:SQLParser.PartitionOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionOption.
    def exitPartitionOption(self, ctx:SQLParser.PartitionOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#subpartitionDefinition.
    def enterSubpartitionDefinition(self, ctx:SQLParser.SubpartitionDefinitionContext):
        pass

    # Exit a parse tree produced by SQLParser#subpartitionDefinition.
    def exitSubpartitionDefinition(self, ctx:SQLParser.SubpartitionDefinitionContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionValueItemListParen.
    def enterPartitionValueItemListParen(self, ctx:SQLParser.PartitionValueItemListParenContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionValueItemListParen.
    def exitPartitionValueItemListParen(self, ctx:SQLParser.PartitionValueItemListParenContext):
        pass


    # Enter a parse tree produced by SQLParser#partitionValueItem.
    def enterPartitionValueItem(self, ctx:SQLParser.PartitionValueItemContext):
        pass

    # Exit a parse tree produced by SQLParser#partitionValueItem.
    def exitPartitionValueItem(self, ctx:SQLParser.PartitionValueItemContext):
        pass


    # Enter a parse tree produced by SQLParser#definerClause.
    def enterDefinerClause(self, ctx:SQLParser.DefinerClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#definerClause.
    def exitDefinerClause(self, ctx:SQLParser.DefinerClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#ifExists.
    def enterIfExists(self, ctx:SQLParser.IfExistsContext):
        pass

    # Exit a parse tree produced by SQLParser#ifExists.
    def exitIfExists(self, ctx:SQLParser.IfExistsContext):
        pass


    # Enter a parse tree produced by SQLParser#ifNotExists.
    def enterIfNotExists(self, ctx:SQLParser.IfNotExistsContext):
        pass

    # Exit a parse tree produced by SQLParser#ifNotExists.
    def exitIfNotExists(self, ctx:SQLParser.IfNotExistsContext):
        pass


    # Enter a parse tree produced by SQLParser#procedureParameter.
    def enterProcedureParameter(self, ctx:SQLParser.ProcedureParameterContext):
        pass

    # Exit a parse tree produced by SQLParser#procedureParameter.
    def exitProcedureParameter(self, ctx:SQLParser.ProcedureParameterContext):
        pass


    # Enter a parse tree produced by SQLParser#functionParameter.
    def enterFunctionParameter(self, ctx:SQLParser.FunctionParameterContext):
        pass

    # Exit a parse tree produced by SQLParser#functionParameter.
    def exitFunctionParameter(self, ctx:SQLParser.FunctionParameterContext):
        pass


    # Enter a parse tree produced by SQLParser#collate.
    def enterCollate(self, ctx:SQLParser.CollateContext):
        pass

    # Exit a parse tree produced by SQLParser#collate.
    def exitCollate(self, ctx:SQLParser.CollateContext):
        pass


    # Enter a parse tree produced by SQLParser#typeWithOptCollate.
    def enterTypeWithOptCollate(self, ctx:SQLParser.TypeWithOptCollateContext):
        pass

    # Exit a parse tree produced by SQLParser#typeWithOptCollate.
    def exitTypeWithOptCollate(self, ctx:SQLParser.TypeWithOptCollateContext):
        pass


    # Enter a parse tree produced by SQLParser#schemaIdentifierPair.
    def enterSchemaIdentifierPair(self, ctx:SQLParser.SchemaIdentifierPairContext):
        pass

    # Exit a parse tree produced by SQLParser#schemaIdentifierPair.
    def exitSchemaIdentifierPair(self, ctx:SQLParser.SchemaIdentifierPairContext):
        pass


    # Enter a parse tree produced by SQLParser#viewRefList.
    def enterViewRefList(self, ctx:SQLParser.ViewRefListContext):
        pass

    # Exit a parse tree produced by SQLParser#viewRefList.
    def exitViewRefList(self, ctx:SQLParser.ViewRefListContext):
        pass


    # Enter a parse tree produced by SQLParser#updateList.
    def enterUpdateList(self, ctx:SQLParser.UpdateListContext):
        pass

    # Exit a parse tree produced by SQLParser#updateList.
    def exitUpdateList(self, ctx:SQLParser.UpdateListContext):
        pass


    # Enter a parse tree produced by SQLParser#updateElement.
    def enterUpdateElement(self, ctx:SQLParser.UpdateElementContext):
        pass

    # Exit a parse tree produced by SQLParser#updateElement.
    def exitUpdateElement(self, ctx:SQLParser.UpdateElementContext):
        pass


    # Enter a parse tree produced by SQLParser#charsetClause.
    def enterCharsetClause(self, ctx:SQLParser.CharsetClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#charsetClause.
    def exitCharsetClause(self, ctx:SQLParser.CharsetClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldsClause.
    def enterFieldsClause(self, ctx:SQLParser.FieldsClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldsClause.
    def exitFieldsClause(self, ctx:SQLParser.FieldsClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldTerm.
    def enterFieldTerm(self, ctx:SQLParser.FieldTermContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldTerm.
    def exitFieldTerm(self, ctx:SQLParser.FieldTermContext):
        pass


    # Enter a parse tree produced by SQLParser#linesClause.
    def enterLinesClause(self, ctx:SQLParser.LinesClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#linesClause.
    def exitLinesClause(self, ctx:SQLParser.LinesClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#lineTerm.
    def enterLineTerm(self, ctx:SQLParser.LineTermContext):
        pass

    # Exit a parse tree produced by SQLParser#lineTerm.
    def exitLineTerm(self, ctx:SQLParser.LineTermContext):
        pass


    # Enter a parse tree produced by SQLParser#userList.
    def enterUserList(self, ctx:SQLParser.UserListContext):
        pass

    # Exit a parse tree produced by SQLParser#userList.
    def exitUserList(self, ctx:SQLParser.UserListContext):
        pass


    # Enter a parse tree produced by SQLParser#createUserList.
    def enterCreateUserList(self, ctx:SQLParser.CreateUserListContext):
        pass

    # Exit a parse tree produced by SQLParser#createUserList.
    def exitCreateUserList(self, ctx:SQLParser.CreateUserListContext):
        pass


    # Enter a parse tree produced by SQLParser#alterUserList.
    def enterAlterUserList(self, ctx:SQLParser.AlterUserListContext):
        pass

    # Exit a parse tree produced by SQLParser#alterUserList.
    def exitAlterUserList(self, ctx:SQLParser.AlterUserListContext):
        pass


    # Enter a parse tree produced by SQLParser#createUserEntry.
    def enterCreateUserEntry(self, ctx:SQLParser.CreateUserEntryContext):
        pass

    # Exit a parse tree produced by SQLParser#createUserEntry.
    def exitCreateUserEntry(self, ctx:SQLParser.CreateUserEntryContext):
        pass


    # Enter a parse tree produced by SQLParser#alterUserEntry.
    def enterAlterUserEntry(self, ctx:SQLParser.AlterUserEntryContext):
        pass

    # Exit a parse tree produced by SQLParser#alterUserEntry.
    def exitAlterUserEntry(self, ctx:SQLParser.AlterUserEntryContext):
        pass


    # Enter a parse tree produced by SQLParser#retainCurrentPassword.
    def enterRetainCurrentPassword(self, ctx:SQLParser.RetainCurrentPasswordContext):
        pass

    # Exit a parse tree produced by SQLParser#retainCurrentPassword.
    def exitRetainCurrentPassword(self, ctx:SQLParser.RetainCurrentPasswordContext):
        pass


    # Enter a parse tree produced by SQLParser#discardOldPassword.
    def enterDiscardOldPassword(self, ctx:SQLParser.DiscardOldPasswordContext):
        pass

    # Exit a parse tree produced by SQLParser#discardOldPassword.
    def exitDiscardOldPassword(self, ctx:SQLParser.DiscardOldPasswordContext):
        pass


    # Enter a parse tree produced by SQLParser#replacePassword.
    def enterReplacePassword(self, ctx:SQLParser.ReplacePasswordContext):
        pass

    # Exit a parse tree produced by SQLParser#replacePassword.
    def exitReplacePassword(self, ctx:SQLParser.ReplacePasswordContext):
        pass


    # Enter a parse tree produced by SQLParser#userIdentifierOrText.
    def enterUserIdentifierOrText(self, ctx:SQLParser.UserIdentifierOrTextContext):
        pass

    # Exit a parse tree produced by SQLParser#userIdentifierOrText.
    def exitUserIdentifierOrText(self, ctx:SQLParser.UserIdentifierOrTextContext):
        pass


    # Enter a parse tree produced by SQLParser#user.
    def enterUser(self, ctx:SQLParser.UserContext):
        pass

    # Exit a parse tree produced by SQLParser#user.
    def exitUser(self, ctx:SQLParser.UserContext):
        pass


    # Enter a parse tree produced by SQLParser#likeClause.
    def enterLikeClause(self, ctx:SQLParser.LikeClauseContext):
        pass

    # Exit a parse tree produced by SQLParser#likeClause.
    def exitLikeClause(self, ctx:SQLParser.LikeClauseContext):
        pass


    # Enter a parse tree produced by SQLParser#likeOrWhere.
    def enterLikeOrWhere(self, ctx:SQLParser.LikeOrWhereContext):
        pass

    # Exit a parse tree produced by SQLParser#likeOrWhere.
    def exitLikeOrWhere(self, ctx:SQLParser.LikeOrWhereContext):
        pass


    # Enter a parse tree produced by SQLParser#onlineOption.
    def enterOnlineOption(self, ctx:SQLParser.OnlineOptionContext):
        pass

    # Exit a parse tree produced by SQLParser#onlineOption.
    def exitOnlineOption(self, ctx:SQLParser.OnlineOptionContext):
        pass


    # Enter a parse tree produced by SQLParser#noWriteToBinLog.
    def enterNoWriteToBinLog(self, ctx:SQLParser.NoWriteToBinLogContext):
        pass

    # Exit a parse tree produced by SQLParser#noWriteToBinLog.
    def exitNoWriteToBinLog(self, ctx:SQLParser.NoWriteToBinLogContext):
        pass


    # Enter a parse tree produced by SQLParser#usePartition.
    def enterUsePartition(self, ctx:SQLParser.UsePartitionContext):
        pass

    # Exit a parse tree produced by SQLParser#usePartition.
    def exitUsePartition(self, ctx:SQLParser.UsePartitionContext):
        pass


    # Enter a parse tree produced by SQLParser#fieldIdentifier.
    def enterFieldIdentifier(self, ctx:SQLParser.FieldIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#fieldIdentifier.
    def exitFieldIdentifier(self, ctx:SQLParser.FieldIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#columnName.
    def enterColumnName(self, ctx:SQLParser.ColumnNameContext):
        pass

    # Exit a parse tree produced by SQLParser#columnName.
    def exitColumnName(self, ctx:SQLParser.ColumnNameContext):
        pass


    # Enter a parse tree produced by SQLParser#columnInternalRef.
    def enterColumnInternalRef(self, ctx:SQLParser.ColumnInternalRefContext):
        pass

    # Exit a parse tree produced by SQLParser#columnInternalRef.
    def exitColumnInternalRef(self, ctx:SQLParser.ColumnInternalRefContext):
        pass


    # Enter a parse tree produced by SQLParser#columnInternalRefList.
    def enterColumnInternalRefList(self, ctx:SQLParser.ColumnInternalRefListContext):
        pass

    # Exit a parse tree produced by SQLParser#columnInternalRefList.
    def exitColumnInternalRefList(self, ctx:SQLParser.ColumnInternalRefListContext):
        pass


    # Enter a parse tree produced by SQLParser#columnRef.
    def enterColumnRef(self, ctx:SQLParser.ColumnRefContext):
        pass

    # Exit a parse tree produced by SQLParser#columnRef.
    def exitColumnRef(self, ctx:SQLParser.ColumnRefContext):
        pass


    # Enter a parse tree produced by SQLParser#insertIdentifier.
    def enterInsertIdentifier(self, ctx:SQLParser.InsertIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#insertIdentifier.
    def exitInsertIdentifier(self, ctx:SQLParser.InsertIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#indexName.
    def enterIndexName(self, ctx:SQLParser.IndexNameContext):
        pass

    # Exit a parse tree produced by SQLParser#indexName.
    def exitIndexName(self, ctx:SQLParser.IndexNameContext):
        pass


    # Enter a parse tree produced by SQLParser#indexRef.
    def enterIndexRef(self, ctx:SQLParser.IndexRefContext):
        pass

    # Exit a parse tree produced by SQLParser#indexRef.
    def exitIndexRef(self, ctx:SQLParser.IndexRefContext):
        pass


    # Enter a parse tree produced by SQLParser#tableWild.
    def enterTableWild(self, ctx:SQLParser.TableWildContext):
        pass

    # Exit a parse tree produced by SQLParser#tableWild.
    def exitTableWild(self, ctx:SQLParser.TableWildContext):
        pass


    # Enter a parse tree produced by SQLParser#schemaName.
    def enterSchemaName(self, ctx:SQLParser.SchemaNameContext):
        pass

    # Exit a parse tree produced by SQLParser#schemaName.
    def exitSchemaName(self, ctx:SQLParser.SchemaNameContext):
        pass


    # Enter a parse tree produced by SQLParser#schemaRef.
    def enterSchemaRef(self, ctx:SQLParser.SchemaRefContext):
        pass

    # Exit a parse tree produced by SQLParser#schemaRef.
    def exitSchemaRef(self, ctx:SQLParser.SchemaRefContext):
        pass


    # Enter a parse tree produced by SQLParser#procedureName.
    def enterProcedureName(self, ctx:SQLParser.ProcedureNameContext):
        pass

    # Exit a parse tree produced by SQLParser#procedureName.
    def exitProcedureName(self, ctx:SQLParser.ProcedureNameContext):
        pass


    # Enter a parse tree produced by SQLParser#procedureRef.
    def enterProcedureRef(self, ctx:SQLParser.ProcedureRefContext):
        pass

    # Exit a parse tree produced by SQLParser#procedureRef.
    def exitProcedureRef(self, ctx:SQLParser.ProcedureRefContext):
        pass


    # Enter a parse tree produced by SQLParser#functionName.
    def enterFunctionName(self, ctx:SQLParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by SQLParser#functionName.
    def exitFunctionName(self, ctx:SQLParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by SQLParser#functionRef.
    def enterFunctionRef(self, ctx:SQLParser.FunctionRefContext):
        pass

    # Exit a parse tree produced by SQLParser#functionRef.
    def exitFunctionRef(self, ctx:SQLParser.FunctionRefContext):
        pass


    # Enter a parse tree produced by SQLParser#triggerName.
    def enterTriggerName(self, ctx:SQLParser.TriggerNameContext):
        pass

    # Exit a parse tree produced by SQLParser#triggerName.
    def exitTriggerName(self, ctx:SQLParser.TriggerNameContext):
        pass


    # Enter a parse tree produced by SQLParser#triggerRef.
    def enterTriggerRef(self, ctx:SQLParser.TriggerRefContext):
        pass

    # Exit a parse tree produced by SQLParser#triggerRef.
    def exitTriggerRef(self, ctx:SQLParser.TriggerRefContext):
        pass


    # Enter a parse tree produced by SQLParser#viewName.
    def enterViewName(self, ctx:SQLParser.ViewNameContext):
        pass

    # Exit a parse tree produced by SQLParser#viewName.
    def exitViewName(self, ctx:SQLParser.ViewNameContext):
        pass


    # Enter a parse tree produced by SQLParser#viewRef.
    def enterViewRef(self, ctx:SQLParser.ViewRefContext):
        pass

    # Exit a parse tree produced by SQLParser#viewRef.
    def exitViewRef(self, ctx:SQLParser.ViewRefContext):
        pass


    # Enter a parse tree produced by SQLParser#tablespaceName.
    def enterTablespaceName(self, ctx:SQLParser.TablespaceNameContext):
        pass

    # Exit a parse tree produced by SQLParser#tablespaceName.
    def exitTablespaceName(self, ctx:SQLParser.TablespaceNameContext):
        pass


    # Enter a parse tree produced by SQLParser#tablespaceRef.
    def enterTablespaceRef(self, ctx:SQLParser.TablespaceRefContext):
        pass

    # Exit a parse tree produced by SQLParser#tablespaceRef.
    def exitTablespaceRef(self, ctx:SQLParser.TablespaceRefContext):
        pass


    # Enter a parse tree produced by SQLParser#logfileGroupName.
    def enterLogfileGroupName(self, ctx:SQLParser.LogfileGroupNameContext):
        pass

    # Exit a parse tree produced by SQLParser#logfileGroupName.
    def exitLogfileGroupName(self, ctx:SQLParser.LogfileGroupNameContext):
        pass


    # Enter a parse tree produced by SQLParser#logfileGroupRef.
    def enterLogfileGroupRef(self, ctx:SQLParser.LogfileGroupRefContext):
        pass

    # Exit a parse tree produced by SQLParser#logfileGroupRef.
    def exitLogfileGroupRef(self, ctx:SQLParser.LogfileGroupRefContext):
        pass


    # Enter a parse tree produced by SQLParser#eventName.
    def enterEventName(self, ctx:SQLParser.EventNameContext):
        pass

    # Exit a parse tree produced by SQLParser#eventName.
    def exitEventName(self, ctx:SQLParser.EventNameContext):
        pass


    # Enter a parse tree produced by SQLParser#eventRef.
    def enterEventRef(self, ctx:SQLParser.EventRefContext):
        pass

    # Exit a parse tree produced by SQLParser#eventRef.
    def exitEventRef(self, ctx:SQLParser.EventRefContext):
        pass


    # Enter a parse tree produced by SQLParser#udfName.
    def enterUdfName(self, ctx:SQLParser.UdfNameContext):
        pass

    # Exit a parse tree produced by SQLParser#udfName.
    def exitUdfName(self, ctx:SQLParser.UdfNameContext):
        pass


    # Enter a parse tree produced by SQLParser#serverName.
    def enterServerName(self, ctx:SQLParser.ServerNameContext):
        pass

    # Exit a parse tree produced by SQLParser#serverName.
    def exitServerName(self, ctx:SQLParser.ServerNameContext):
        pass


    # Enter a parse tree produced by SQLParser#serverRef.
    def enterServerRef(self, ctx:SQLParser.ServerRefContext):
        pass

    # Exit a parse tree produced by SQLParser#serverRef.
    def exitServerRef(self, ctx:SQLParser.ServerRefContext):
        pass


    # Enter a parse tree produced by SQLParser#engineRef.
    def enterEngineRef(self, ctx:SQLParser.EngineRefContext):
        pass

    # Exit a parse tree produced by SQLParser#engineRef.
    def exitEngineRef(self, ctx:SQLParser.EngineRefContext):
        pass


    # Enter a parse tree produced by SQLParser#tableName.
    def enterTableName(self, ctx:SQLParser.TableNameContext):
        pass

    # Exit a parse tree produced by SQLParser#tableName.
    def exitTableName(self, ctx:SQLParser.TableNameContext):
        pass


    # Enter a parse tree produced by SQLParser#filterTableRef.
    def enterFilterTableRef(self, ctx:SQLParser.FilterTableRefContext):
        pass

    # Exit a parse tree produced by SQLParser#filterTableRef.
    def exitFilterTableRef(self, ctx:SQLParser.FilterTableRefContext):
        pass


    # Enter a parse tree produced by SQLParser#tableRefWithWildcard.
    def enterTableRefWithWildcard(self, ctx:SQLParser.TableRefWithWildcardContext):
        pass

    # Exit a parse tree produced by SQLParser#tableRefWithWildcard.
    def exitTableRefWithWildcard(self, ctx:SQLParser.TableRefWithWildcardContext):
        pass


    # Enter a parse tree produced by SQLParser#tableRef.
    def enterTableRef(self, ctx:SQLParser.TableRefContext):
        pass

    # Exit a parse tree produced by SQLParser#tableRef.
    def exitTableRef(self, ctx:SQLParser.TableRefContext):
        pass


    # Enter a parse tree produced by SQLParser#tableRefList.
    def enterTableRefList(self, ctx:SQLParser.TableRefListContext):
        pass

    # Exit a parse tree produced by SQLParser#tableRefList.
    def exitTableRefList(self, ctx:SQLParser.TableRefListContext):
        pass


    # Enter a parse tree produced by SQLParser#tableAliasRefList.
    def enterTableAliasRefList(self, ctx:SQLParser.TableAliasRefListContext):
        pass

    # Exit a parse tree produced by SQLParser#tableAliasRefList.
    def exitTableAliasRefList(self, ctx:SQLParser.TableAliasRefListContext):
        pass


    # Enter a parse tree produced by SQLParser#parameterName.
    def enterParameterName(self, ctx:SQLParser.ParameterNameContext):
        pass

    # Exit a parse tree produced by SQLParser#parameterName.
    def exitParameterName(self, ctx:SQLParser.ParameterNameContext):
        pass


    # Enter a parse tree produced by SQLParser#labelIdentifier.
    def enterLabelIdentifier(self, ctx:SQLParser.LabelIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#labelIdentifier.
    def exitLabelIdentifier(self, ctx:SQLParser.LabelIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#labelRef.
    def enterLabelRef(self, ctx:SQLParser.LabelRefContext):
        pass

    # Exit a parse tree produced by SQLParser#labelRef.
    def exitLabelRef(self, ctx:SQLParser.LabelRefContext):
        pass


    # Enter a parse tree produced by SQLParser#roleIdentifier.
    def enterRoleIdentifier(self, ctx:SQLParser.RoleIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#roleIdentifier.
    def exitRoleIdentifier(self, ctx:SQLParser.RoleIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#roleRef.
    def enterRoleRef(self, ctx:SQLParser.RoleRefContext):
        pass

    # Exit a parse tree produced by SQLParser#roleRef.
    def exitRoleRef(self, ctx:SQLParser.RoleRefContext):
        pass


    # Enter a parse tree produced by SQLParser#pluginRef.
    def enterPluginRef(self, ctx:SQLParser.PluginRefContext):
        pass

    # Exit a parse tree produced by SQLParser#pluginRef.
    def exitPluginRef(self, ctx:SQLParser.PluginRefContext):
        pass


    # Enter a parse tree produced by SQLParser#componentRef.
    def enterComponentRef(self, ctx:SQLParser.ComponentRefContext):
        pass

    # Exit a parse tree produced by SQLParser#componentRef.
    def exitComponentRef(self, ctx:SQLParser.ComponentRefContext):
        pass


    # Enter a parse tree produced by SQLParser#resourceGroupRef.
    def enterResourceGroupRef(self, ctx:SQLParser.ResourceGroupRefContext):
        pass

    # Exit a parse tree produced by SQLParser#resourceGroupRef.
    def exitResourceGroupRef(self, ctx:SQLParser.ResourceGroupRefContext):
        pass


    # Enter a parse tree produced by SQLParser#windowName.
    def enterWindowName(self, ctx:SQLParser.WindowNameContext):
        pass

    # Exit a parse tree produced by SQLParser#windowName.
    def exitWindowName(self, ctx:SQLParser.WindowNameContext):
        pass


    # Enter a parse tree produced by SQLParser#pureIdentifier.
    def enterPureIdentifier(self, ctx:SQLParser.PureIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#pureIdentifier.
    def exitPureIdentifier(self, ctx:SQLParser.PureIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#identifier.
    def enterIdentifier(self, ctx:SQLParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#identifier.
    def exitIdentifier(self, ctx:SQLParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierList.
    def enterIdentifierList(self, ctx:SQLParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierList.
    def exitIdentifierList(self, ctx:SQLParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierListWithParentheses.
    def enterIdentifierListWithParentheses(self, ctx:SQLParser.IdentifierListWithParenthesesContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierListWithParentheses.
    def exitIdentifierListWithParentheses(self, ctx:SQLParser.IdentifierListWithParenthesesContext):
        pass


    # Enter a parse tree produced by SQLParser#qualifiedIdentifier.
    def enterQualifiedIdentifier(self, ctx:SQLParser.QualifiedIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#qualifiedIdentifier.
    def exitQualifiedIdentifier(self, ctx:SQLParser.QualifiedIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#simpleIdentifier.
    def enterSimpleIdentifier(self, ctx:SQLParser.SimpleIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#simpleIdentifier.
    def exitSimpleIdentifier(self, ctx:SQLParser.SimpleIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#dotIdentifier.
    def enterDotIdentifier(self, ctx:SQLParser.DotIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#dotIdentifier.
    def exitDotIdentifier(self, ctx:SQLParser.DotIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#ulong_number.
    def enterUlong_number(self, ctx:SQLParser.Ulong_numberContext):
        pass

    # Exit a parse tree produced by SQLParser#ulong_number.
    def exitUlong_number(self, ctx:SQLParser.Ulong_numberContext):
        pass


    # Enter a parse tree produced by SQLParser#real_ulong_number.
    def enterReal_ulong_number(self, ctx:SQLParser.Real_ulong_numberContext):
        pass

    # Exit a parse tree produced by SQLParser#real_ulong_number.
    def exitReal_ulong_number(self, ctx:SQLParser.Real_ulong_numberContext):
        pass


    # Enter a parse tree produced by SQLParser#ulonglong_number.
    def enterUlonglong_number(self, ctx:SQLParser.Ulonglong_numberContext):
        pass

    # Exit a parse tree produced by SQLParser#ulonglong_number.
    def exitUlonglong_number(self, ctx:SQLParser.Ulonglong_numberContext):
        pass


    # Enter a parse tree produced by SQLParser#real_ulonglong_number.
    def enterReal_ulonglong_number(self, ctx:SQLParser.Real_ulonglong_numberContext):
        pass

    # Exit a parse tree produced by SQLParser#real_ulonglong_number.
    def exitReal_ulonglong_number(self, ctx:SQLParser.Real_ulonglong_numberContext):
        pass


    # Enter a parse tree produced by SQLParser#literal.
    def enterLiteral(self, ctx:SQLParser.LiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#literal.
    def exitLiteral(self, ctx:SQLParser.LiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#signedLiteral.
    def enterSignedLiteral(self, ctx:SQLParser.SignedLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#signedLiteral.
    def exitSignedLiteral(self, ctx:SQLParser.SignedLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#stringList.
    def enterStringList(self, ctx:SQLParser.StringListContext):
        pass

    # Exit a parse tree produced by SQLParser#stringList.
    def exitStringList(self, ctx:SQLParser.StringListContext):
        pass


    # Enter a parse tree produced by SQLParser#textStringLiteral.
    def enterTextStringLiteral(self, ctx:SQLParser.TextStringLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#textStringLiteral.
    def exitTextStringLiteral(self, ctx:SQLParser.TextStringLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#textString.
    def enterTextString(self, ctx:SQLParser.TextStringContext):
        pass

    # Exit a parse tree produced by SQLParser#textString.
    def exitTextString(self, ctx:SQLParser.TextStringContext):
        pass


    # Enter a parse tree produced by SQLParser#textStringHash.
    def enterTextStringHash(self, ctx:SQLParser.TextStringHashContext):
        pass

    # Exit a parse tree produced by SQLParser#textStringHash.
    def exitTextStringHash(self, ctx:SQLParser.TextStringHashContext):
        pass


    # Enter a parse tree produced by SQLParser#textLiteral.
    def enterTextLiteral(self, ctx:SQLParser.TextLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#textLiteral.
    def exitTextLiteral(self, ctx:SQLParser.TextLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#textStringNoLinebreak.
    def enterTextStringNoLinebreak(self, ctx:SQLParser.TextStringNoLinebreakContext):
        pass

    # Exit a parse tree produced by SQLParser#textStringNoLinebreak.
    def exitTextStringNoLinebreak(self, ctx:SQLParser.TextStringNoLinebreakContext):
        pass


    # Enter a parse tree produced by SQLParser#textStringLiteralList.
    def enterTextStringLiteralList(self, ctx:SQLParser.TextStringLiteralListContext):
        pass

    # Exit a parse tree produced by SQLParser#textStringLiteralList.
    def exitTextStringLiteralList(self, ctx:SQLParser.TextStringLiteralListContext):
        pass


    # Enter a parse tree produced by SQLParser#numLiteral.
    def enterNumLiteral(self, ctx:SQLParser.NumLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#numLiteral.
    def exitNumLiteral(self, ctx:SQLParser.NumLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#boolLiteral.
    def enterBoolLiteral(self, ctx:SQLParser.BoolLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#boolLiteral.
    def exitBoolLiteral(self, ctx:SQLParser.BoolLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#nullLiteral.
    def enterNullLiteral(self, ctx:SQLParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#nullLiteral.
    def exitNullLiteral(self, ctx:SQLParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#temporalLiteral.
    def enterTemporalLiteral(self, ctx:SQLParser.TemporalLiteralContext):
        pass

    # Exit a parse tree produced by SQLParser#temporalLiteral.
    def exitTemporalLiteral(self, ctx:SQLParser.TemporalLiteralContext):
        pass


    # Enter a parse tree produced by SQLParser#floatOptions.
    def enterFloatOptions(self, ctx:SQLParser.FloatOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#floatOptions.
    def exitFloatOptions(self, ctx:SQLParser.FloatOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#standardFloatOptions.
    def enterStandardFloatOptions(self, ctx:SQLParser.StandardFloatOptionsContext):
        pass

    # Exit a parse tree produced by SQLParser#standardFloatOptions.
    def exitStandardFloatOptions(self, ctx:SQLParser.StandardFloatOptionsContext):
        pass


    # Enter a parse tree produced by SQLParser#precision.
    def enterPrecision(self, ctx:SQLParser.PrecisionContext):
        pass

    # Exit a parse tree produced by SQLParser#precision.
    def exitPrecision(self, ctx:SQLParser.PrecisionContext):
        pass


    # Enter a parse tree produced by SQLParser#textOrIdentifier.
    def enterTextOrIdentifier(self, ctx:SQLParser.TextOrIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#textOrIdentifier.
    def exitTextOrIdentifier(self, ctx:SQLParser.TextOrIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#lValueIdentifier.
    def enterLValueIdentifier(self, ctx:SQLParser.LValueIdentifierContext):
        pass

    # Exit a parse tree produced by SQLParser#lValueIdentifier.
    def exitLValueIdentifier(self, ctx:SQLParser.LValueIdentifierContext):
        pass


    # Enter a parse tree produced by SQLParser#roleIdentifierOrText.
    def enterRoleIdentifierOrText(self, ctx:SQLParser.RoleIdentifierOrTextContext):
        pass

    # Exit a parse tree produced by SQLParser#roleIdentifierOrText.
    def exitRoleIdentifierOrText(self, ctx:SQLParser.RoleIdentifierOrTextContext):
        pass


    # Enter a parse tree produced by SQLParser#sizeNumber.
    def enterSizeNumber(self, ctx:SQLParser.SizeNumberContext):
        pass

    # Exit a parse tree produced by SQLParser#sizeNumber.
    def exitSizeNumber(self, ctx:SQLParser.SizeNumberContext):
        pass


    # Enter a parse tree produced by SQLParser#parentheses.
    def enterParentheses(self, ctx:SQLParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by SQLParser#parentheses.
    def exitParentheses(self, ctx:SQLParser.ParenthesesContext):
        pass


    # Enter a parse tree produced by SQLParser#equal.
    def enterEqual(self, ctx:SQLParser.EqualContext):
        pass

    # Exit a parse tree produced by SQLParser#equal.
    def exitEqual(self, ctx:SQLParser.EqualContext):
        pass


    # Enter a parse tree produced by SQLParser#optionType.
    def enterOptionType(self, ctx:SQLParser.OptionTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#optionType.
    def exitOptionType(self, ctx:SQLParser.OptionTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#varIdentType.
    def enterVarIdentType(self, ctx:SQLParser.VarIdentTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#varIdentType.
    def exitVarIdentType(self, ctx:SQLParser.VarIdentTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#setVarIdentType.
    def enterSetVarIdentType(self, ctx:SQLParser.SetVarIdentTypeContext):
        pass

    # Exit a parse tree produced by SQLParser#setVarIdentType.
    def exitSetVarIdentType(self, ctx:SQLParser.SetVarIdentTypeContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeyword.
    def enterIdentifierKeyword(self, ctx:SQLParser.IdentifierKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeyword.
    def exitIdentifierKeyword(self, ctx:SQLParser.IdentifierKeywordContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeywordsAmbiguous1RolesAndLabels.
    def enterIdentifierKeywordsAmbiguous1RolesAndLabels(self, ctx:SQLParser.IdentifierKeywordsAmbiguous1RolesAndLabelsContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeywordsAmbiguous1RolesAndLabels.
    def exitIdentifierKeywordsAmbiguous1RolesAndLabels(self, ctx:SQLParser.IdentifierKeywordsAmbiguous1RolesAndLabelsContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeywordsAmbiguous2Labels.
    def enterIdentifierKeywordsAmbiguous2Labels(self, ctx:SQLParser.IdentifierKeywordsAmbiguous2LabelsContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeywordsAmbiguous2Labels.
    def exitIdentifierKeywordsAmbiguous2Labels(self, ctx:SQLParser.IdentifierKeywordsAmbiguous2LabelsContext):
        pass


    # Enter a parse tree produced by SQLParser#labelKeyword.
    def enterLabelKeyword(self, ctx:SQLParser.LabelKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#labelKeyword.
    def exitLabelKeyword(self, ctx:SQLParser.LabelKeywordContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeywordsAmbiguous3Roles.
    def enterIdentifierKeywordsAmbiguous3Roles(self, ctx:SQLParser.IdentifierKeywordsAmbiguous3RolesContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeywordsAmbiguous3Roles.
    def exitIdentifierKeywordsAmbiguous3Roles(self, ctx:SQLParser.IdentifierKeywordsAmbiguous3RolesContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeywordsUnambiguous.
    def enterIdentifierKeywordsUnambiguous(self, ctx:SQLParser.IdentifierKeywordsUnambiguousContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeywordsUnambiguous.
    def exitIdentifierKeywordsUnambiguous(self, ctx:SQLParser.IdentifierKeywordsUnambiguousContext):
        pass


    # Enter a parse tree produced by SQLParser#roleKeyword.
    def enterRoleKeyword(self, ctx:SQLParser.RoleKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#roleKeyword.
    def exitRoleKeyword(self, ctx:SQLParser.RoleKeywordContext):
        pass


    # Enter a parse tree produced by SQLParser#lValueKeyword.
    def enterLValueKeyword(self, ctx:SQLParser.LValueKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#lValueKeyword.
    def exitLValueKeyword(self, ctx:SQLParser.LValueKeywordContext):
        pass


    # Enter a parse tree produced by SQLParser#identifierKeywordsAmbiguous4SystemVariables.
    def enterIdentifierKeywordsAmbiguous4SystemVariables(self, ctx:SQLParser.IdentifierKeywordsAmbiguous4SystemVariablesContext):
        pass

    # Exit a parse tree produced by SQLParser#identifierKeywordsAmbiguous4SystemVariables.
    def exitIdentifierKeywordsAmbiguous4SystemVariables(self, ctx:SQLParser.IdentifierKeywordsAmbiguous4SystemVariablesContext):
        pass


    # Enter a parse tree produced by SQLParser#roleOrIdentifierKeyword.
    def enterRoleOrIdentifierKeyword(self, ctx:SQLParser.RoleOrIdentifierKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#roleOrIdentifierKeyword.
    def exitRoleOrIdentifierKeyword(self, ctx:SQLParser.RoleOrIdentifierKeywordContext):
        pass


    # Enter a parse tree produced by SQLParser#roleOrLabelKeyword.
    def enterRoleOrLabelKeyword(self, ctx:SQLParser.RoleOrLabelKeywordContext):
        pass

    # Exit a parse tree produced by SQLParser#roleOrLabelKeyword.
    def exitRoleOrLabelKeyword(self, ctx:SQLParser.RoleOrLabelKeywordContext):
        pass



del SQLParser